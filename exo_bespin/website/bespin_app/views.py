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

from django.http import HttpResponse
from django.http import HttpRequest as request
from django.shortcuts import render

from exo_bespin.aws import aws_tools


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

    template = 'home.html'
    context = {}

    return render(request, template, context)


def results(request):
    """
    """

    template = 'results.html'
    context = {}

    return render(request, template, context)


def _ajax_results(request):
    """
    """

    ssh_file = aws_tools.get_config()['ssh_file']
    ec2_id = aws_tools.get_config()['ec2_id']

    instance, key, client = aws_tools.start_ec2(ssh_file, ec2_id)
    aws_tools.wait_for_instance(instance, key, client)

    command = './exo_bespin/exo_bespin/aws/exo_bespin-env-init.sh python exo_bespin/exo_bespin/examples/ec2_example.py'
    output, errors = aws_tools.run_command(command, instance, key, client)
    for line in output:
        print(line)

    aws_tools.transfer_from_ec2(instance, key, client, 'results/lc.dat')

    aws_tools.stop_ec2(ec2_id, instance)

    return HttpResponse('Process complete')
