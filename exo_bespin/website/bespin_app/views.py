"""Defines the views for the ``bespin`` web app.

In Django, "a view function, or view for short, is simply a Python
function that takes a Web request and returns a Web response" (from
Django documentation). This module defines all of the views that are
used to generate the various webpages used for the ``bespin``
application.

Authors
-------

    - Matthew Bourque

Use
---

    This module is called in ``urls.py`` as such:
    ::

        from django.urls import path
        from . import views
        urlpatterns = [path('web/path/to/view/', views.view_name,
        name='view_name')]

References
----------
    For more information please see:
        ``https://docs.djangoproject.com/en/2.0/topics/http/views/``

Dependencies
------------

    - ``django``

"""

import json
import os

from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpRequest as request
from django.shortcuts import render

from exo_bespin.aws import aws_tools
from exo_bespin.website.bespin_app.form_validation import ExampleForm


def _process_request(form):
    """
    """

    # Get the parameters from the form and save them to a json file
    params = form.get_cleaned_data()
    params_file = os.path.join(os.path.expanduser("~"), 'params.json')
    with open(params_file, 'w') as f:
        json.dump(params, f)

    # Get info from config file
    ssh_file = aws_tools.get_config()['ssh_file']
    ec2_id = aws_tools.get_config()['ec2_id']

    # Boot up the EC2 instance
    instance, key, client = aws_tools.start_ec2(ssh_file, ec2_id)
    aws_tools.wait_for_instance(instance, key, client)

    # Transfer the parameter file to EC2
    aws_tools.transfer_to_ec2(instance, key, client, params_file)

    # Run the code on EC2
    command = './exo_bespin/exo_bespin/aws/exo_bespin-env-init.sh python exo_bespin/run_fit.py'
    output, errors = aws_tools.run_command(command, instance, key, client)
    for line in output:
        print(line)

    # # Get the results back
    # aws_tools.transfer_from_ec2(instance, key, client, 'results/lc.dat')

    # # Stop the EC2 instance
    # aws_tools.stop_ec2(ec2_id, instance)

    # Parse the results
    results = {}

    return results


def home(request):
    """Generate the home page.

    Parameters
    ----------
    request : HttpRequest object
        Incoming request from the webpage

    Returns
    -------
    HttpResponse object
        Outgoing response sent to the webpage
    """

    if request.method == 'GET':
        form = ExampleForm()
        template = 'home.html'
        context = {'form': form}
        return render(request, template, context)

    elif request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            results = _process_request(form)
            context = {'results': results}
            return render(request, 'results.html', context)
        else:
            context = {}
            return render(request, '404.html', context)

    else:
        context = {}
        return render(request, '404.html', context)
