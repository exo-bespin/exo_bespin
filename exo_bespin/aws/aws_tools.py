"""This module contains various functions for interacting with AWS EC2
instances

Authors
-------

    - Matthew Bourque

Use
---

    This script is inteneded to be imported and used by other modules,
    for example:

        from exo_bespin.aws.aws_tools import get_config
        get_config()

Dependencies
------------

    Dependent libraries include:

    - boto3
    - paramiko
    - scp

    Users must also have a ``aws_config.json`` file present within the
    ``aws`` subdirectory.  This file must be of a valid JSON format and
    contain two key/value pairs, ``ec2_id`` and ``ssh_file``, e.g.:

    {
    "ec2_id" : "lt-021de8b904bc2b728",
    "ssh_file" : "~/.ssh/my_ssh_key.pem"
    }

    where the ``ec2_id`` contains the ID for an EC2 launch template
    or an existing EC2 instance, and ``ssh_file`` points to the SSH
    public key used for logging into an AWS account.
"""

import base64
import json
import logging
import os
import time

import boto3
import paramiko
from scp import SCPClient


def build_environment(instance, key, client):
    """Builds an ``exo-bespin`` environment on the given AWS EC2 instance

    Parameters
    ----------
    instance : obj
        A ``boto3`` AWS EC2 instance object.
    key : obj
        A ``paramiko.rsakey.RSAKey`` object.
    client : obj
        A ``paramiko.client.SSHClient`` object.
    """

    logging.info('Building exo-bespin environment')

    # Connect to the EC2 instance and run commands
    connected = False
    iterations = 0
    while not connected:
        if iterations == 12:
            logging.critical('Could not connect to {}'.format(instance.public_dns_name))
            break
        try:
            client.connect(hostname=instance.public_dns_name, username='ec2-user', pkey=key)
            scp = SCPClient(client.get_transport())
            scp.put('build-exo_bespin-env-cpu.sh', '~/build-exo_bespin-env-cpu.sh')
            stdin, stdout, stderr = client.exec_command('chmod 700 build-exo_bespin-env-cpu.sh && ./build-exo_bespin-env-cpu.sh')
            connected = True
        except:
            iterations += 1
            time.sleep(5)

    output = stdout.read()
    log_output(output)


def create_ec2_launch_template(platform='linux'):
    """Creates an ``exo-besin`` EC2 launch template

    Parameters
    ----------
    platform : str
        The operating system to use.  Must be either ``linux`` or
        ``ubuntu``
    """

    assert platform in ['linux', 'ubuntu'], 'Provided platform must be either "linux" or "ubuntu"'

    if platform == 'linux':
        ami = 'ami-098f16afa9edf40be'
    elif platform == 'ubuntu':
        ami = 'ami-0dba2cb6798deb6d8'

    # Gather user data and encode with base 64
    with open('build-exo_bespin-env-cpu.sh', 'r') as f:
        user_data = f.read()
    user_data = user_data.encode('ascii')
    user_data = base64.b64encode(user_data)
    user_data = user_data.decode('ascii')

    # Create launch template
    client = boto3.client('ec2')
    response = client.create_launch_template(
        LaunchTemplateName=f'exo-bespin-lt-{platform}',
        LaunchTemplateData={
            'ImageId': ami,
            'InstanceType': 't2.medium',
            'KeyName': get_config()['key_pair_name'],
            'UserData': user_data,
            'SecurityGroupIds': [get_config()['security_group_id'], ],
            'BlockDeviceMappings': [{
                'DeviceName': '/dev/sda1',
                'Ebs': {
                    'Encrypted': False,
                    'DeleteOnTermination': True,
                    'SnapshotId': 'snap-0c4e8263cef786d91',
                    'VolumeSize': 20,
                    'VolumeType': 'gp2'},
            }, ],
        },
    )

    print('\nCreated EC2 Launch Template:\n\n{}\n'.format(response))


def get_config():
    """Return a dictionary that holds the contents of the
    ``aws_config.json`` config file.

    Returns
    -------
    settings : dict
        A dictionary that holds the contents of the config file.
    """

    config_file_location = os.path.join(os.path.dirname(__file__), 'aws_config.json')

    if not os.path.isfile(config_file_location):
        raise FileNotFoundError('Missing AWS configuration file ("aws_config.json")')

    with open(config_file_location, 'r') as config_file:
        settings = json.load(config_file)

    return settings


def log_output(output):
    """Logs the given output of the EC2 instance.

    Parameters
    ----------
    output : str
        The standard output of the EC2 instance
    """

    output = output.decode("utf-8")
    output = output.replace('\t', '  ').replace('\r', '').replace("\'", "").split('\n')
    for line in output:
        logging.info(line)


def run_command(command, instance, key, client):
    """Executes the given command on the given EC2 instance

    Parameters
    ----------
    command : str
        The command to run (e.g. ``python run_myscript.py``)
    instance : obj
        A ``boto3`` AWS EC2 instance object.
    key : obj
        A ``paramiko.rsakey.RSAKey`` object.
    client : obj
        A ``paramiko.client.SSHClient`` object.

    Returns
    -------
    output : str
        The standard output from running the command
    errors : str
        The standard error output from running the command
    """

    client.connect(hostname=instance.public_dns_name, username='ec2-user', pkey=key)
    stdin, stdout, stderr = client.exec_command(command)
    output = stdout.read()
    errors = stderr.read()

    # Make output a more readable
    output = output.decode("utf-8")
    output = output.replace('\t', '  ').replace('\r', '').replace("\'", "").split('\n')
    errors = errors.decode("utf-8")
    errors = errors.replace('\t', '  ').replace('\r', '').replace("\'", "").split('\n')

    return output, errors


def start_ec2(ssh_file, ec2_id):
    """Create a new EC2 instance or start an existing EC2 instance.

    A new EC2 instance will be created if the supplied ``ec2_id`` is an
    EC2 template ID.  An existing EC2 instance will be started if the
    supplied ``ec2_id`` is an ID for an existing EC2 instance.

    Parameters
    ----------
    ssh_file : str
        Relative path to SSH public key to be used by AWS (e.g.
        ``~/.ssh/exo_bespin.pem``).
    ec2_id : str
        The AWS EC2 template id (e.g. ``lt-021de8b904bc2b728``) or
        instance ID (e.g. ``i-0d0c8ca4ab324b260``).

    Returns
    -------
    instance : obj
        A ``boto3`` AWS EC2 instance object.
    key : obj
        A ``paramiko.rsakey.RSAKey`` object.
    client : obj
        A ``paramiko.client.SSHClient`` object.
    """

    ec2 = boto3.resource('ec2')

    # If the given ec2_id is for an EC2 template, then create the EC2 instance
    if ec2_id.split('-')[0] == 'lt':
        LaunchTemplate = {'LaunchTemplateId': ec2_id}
        instances = ec2.create_instances(
            LaunchTemplate=LaunchTemplate,
            MaxCount=1,
            MinCount=1)
        instance = instances[0]
        logging.info('Launched EC2 instance {}'.format(instance.id))

    # If the given ec2_id is for an existing EC2 instance, then start it
    else:
        instance = ec2.Instance(ec2_id)
        instance.start()
        logging.info('Started EC2 instance {}'.format(ec2_id))

    instance.wait_until_running()
    instance.load()

    # Establish SSH key and client
    key = paramiko.RSAKey.from_private_key_file(ssh_file)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    return instance, key, client


def stop_ec2(ec2_id, instance):
    """Terminates or stops the given AWS EC2 instance.

    The instance is terminated if the supplied ``ec2_id`` is a EC2
    template ID.  The instance is stopped if the supplied ``ec2_id``
    is an ID for a particular EC2 instance.

    Parameters
    ----------
    ec2_id : str
        The AWS EC2 template id (e.g. ``lt-021de8b904bc2b728``) or
        instance ID (e.g. ``i-0d0c8ca4ab324b260``).
    instance : obj
        A ``boto3`` AWS EC2 instance object.
    """

    ec2 = boto3.resource('ec2')

    # If the given ec2_id is for an EC2 template, then terminate the EC2 instance
    if ec2_id.split('-')[0] == 'lt':
        ec2.instances.filter(InstanceIds=[instance.id]).terminate()
        logging.info('Terminated EC2 instance {}'.format(instance.id))

    # If the given ec2_id is for an existing EC2 instance, then stop it
    else:
        instance.stop()
        logging.info('Stopped EC2 instance {}'.format(ec2_id))


def transfer_from_ec2(instance, key, client, filename):
    """Copy files from EC2 user back to the user

    Parameters
    ----------
    instance : obj
        A ``boto3`` AWS EC2 instance object.
    key : obj
        A ``paramiko.rsakey.RSAKey`` object.
    client : obj
        A ``paramiko.client.SSHClient`` object.
    filename : str
        The path to the file to transfer
    """

    logging.info('Copying {} from EC2'.format(filename))

    client.connect(hostname=instance.public_dns_name, username='ec2-user', pkey=key)
    scp = SCPClient(client.get_transport())
    scp.get(filename)


def transfer_to_ec2(instance, key, client, filename):
    """Copy parameter file from user to EC2 instance

    Parameters
    ----------
    instance : obj
        A ``boto3`` AWS EC2 instance object.
    key : obj
        A ``paramiko.rsakey.RSAKey`` object.
    client : obj
        A ``paramiko.client.SSHClient`` object.
    filename : str
        The path to the file to transfer
    """

    logging.info('Copying {} to EC2'.format(filename))

    connected = False
    iterations = 0
    while not connected:
        if iterations >= 10:
            logging.critical('Could not connect to {}'.format(instance.public_dns_name))
            break
        try:
            client.connect(hostname=instance.public_dns_name, username='ec2-user', pkey=key)
            scp = SCPClient(client.get_transport())
            scp.put(filename)
            connected = True
        except:
            logging.warning('Could not connect to {}, retrying.'.format(instance.public_dns_name))
            time.sleep(5)
            iterations += 1


def wait_for_file(instance, key, client, filename):
    """Waits for the existance of the given ``filename`` on the given
    EC2 instance before proceeding.

    The given ``filename`` must be a full path to the file of interest
    relative to the EC2 instance's ``$HOME`` directory.  For example,
    supplying ``foo.txt`` will look for ``/home/ec2-user/foo.txt``, and
    supplying ``my_dir/bar.txt`` will look for
    ``/home/ec2-user/my_dir/bar.txt``.

    Note that this function assumes that the EC2 instsance is already
    up and running, so users should be careful about the timing and
    placement of this function in their code.

    Parameters
    ----------
    instance : obj
        A ``boto3`` AWS EC2 instance object.
    key : obj
        A ``paramiko.rsakey.RSAKey`` object.
    client : obj
        A ``paramiko.client.SSHClient`` object.
    filename : str
        The filename of interest
    """

    file_exists = False
    iteration = 0

    while not file_exists:

        if iteration == 100:
            print('Timeout encountered when waiting for {} to be ready'.format(instance.public_dns_name))
            break

        try:
            output, errors = run_command('ls {}'.format(filename), instance, key, client)
            if os.path.basename(filename) in output:
                file_exists = True
            else:
                iteration += 1
                time.sleep(10)
        except:
            iteration += 1
            time.sleep(10)


def wait_for_instance(instance, key, client):
    """Waits for the given EC2 instance to be completely set up with
    the `exo_bespin` software environment.

    The `exo_bespin` software environment is considered complete when
    the `cloud-init-output.log` file exists in the instance's home
    directory, as the last step in the build process is to copy that
    file there (see `build-exo_bespin-env-cpu.sh`).

    Parameters
    ----------
    instance : obj
        A ``boto3`` AWS EC2 instance object.
    key : obj
        A ``paramiko.rsakey.RSAKey`` object.
    client : obj
        A ``paramiko.client.SSHClient`` object.
    """

    wait_for_file(instance, key, client, 'cloud-init-output.log')


if __name__ == '__main__':

    create_ec2_launch_template()
