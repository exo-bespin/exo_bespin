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

"""

from django.http import HttpRequest as request
from django.shortcuts import render


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
