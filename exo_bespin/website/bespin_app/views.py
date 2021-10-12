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
import shutil

from django.http import HttpRequest as request
from django.shortcuts import render

from exo_bespin.aws import aws_tools
from exo_bespin.website.bespin_app.form_validation import LightcurveForm


def _process_request(form, user_uploaded_file):
    """Gather parameters given by the user, run the fit, and move the
    results to be rendered by the web app.

    Parameters
    ----------
    form : ``django.form.Forms`` object
        The form that contains user-provided parameters
    user_uploaded_file : `InMemoryUploadedFile`
        The user-provided file that contains lightcurve data
    """

    # Get the parameters from the form and save them to a json file
    params = form.get_cleaned_data()
    del params['filename']
    params_file = os.path.join(os.path.expanduser("~"), 'params.json')
    with open(params_file, 'w') as f:
        json.dump(params, f, indent=2)

    # Save a copy of the user-uploaded file
    lightcurve_data_file = os.path.join(os.path.expanduser("~"), 'lightcurve.dat')
    with open(lightcurve_data_file, 'wb+') as destination:
        for chunk in user_uploaded_file.chunks():
            destination.write(chunk)

    # Get info from config file
    ssh_file = aws_tools.get_config()['ssh_file']
    ec2_id = aws_tools.get_config()['ec2_id']

    # Boot up the EC2 instance
    instance, key, client = aws_tools.start_ec2(ssh_file, ec2_id)
    aws_tools.wait_for_instance(instance, key, client)

    # Transfer the parameter and lightcurve data files to EC2
    aws_tools.transfer_to_ec2(instance, key, client, params_file)
    aws_tools.transfer_to_ec2(instance, key, client, lightcurve_data_file)

    # Run the code on EC2
    command = './exo_bespin/exo_bespin/aws/exo_bespin-env-init.sh python exo_bespin/run_fit.py'
    output, errors = aws_tools.run_command(command, instance, key, client)

    # Get the results back
    aws_tools.transfer_from_ec2(instance, key, client, 'transit_fit.png')
    aws_tools.transfer_from_ec2(instance, key, client, 'corner_plot.png')

    # Stop the EC2 instance
    aws_tools.stop_ec2(ec2_id, instance)

    # Move the results to within the application
    shutil.move('transit_fit.png', 'bespin_app/static/img/transit_fit.png')
    shutil.move('corner_plot.png', 'bespin_app/static/img/corner_plot.png')


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
        form = LightcurveForm()
        template = 'home.html'
        context = {'form': form}
        return render(request, template, context)

    elif request.method == 'POST':
        form = LightcurveForm(request.POST, request.FILES)
        print(request.FILES)
        if form.is_valid():
            user_uploaded_file = request.FILES['filename']
            print(user_uploaded_file)
            results = _process_request(form, user_uploaded_file)
            context = {'results': results}
            return render(request, 'results.html', context)
        else:
            context = {}
            return render(request, '404.html', context)

    else:
        context = {}
        return render(request, '404.html', context)
