"""Maps URL paths to views in the ``bespin`` app.

This module connects requested URL paths to the corresponding view in
``views.py`` for each webpage in the ``bespin`` app. When django is
provided a path, it searches through the ``urlpatterns`` list provided
here until it finds one that matches. It then calls the assigned view
to load the appropriate webpage, passing an ``HttpRequest`` object.

Authors
-------

    - Matthew Bourque

Use
---

    Function views
        1. Add an import:  from my_app import views
        2. Add a URL to urlpatterns:  path('', views.home, name='home')
    Class-based views
        1. Add an import:  from other_app.views import Home
        2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
    Including another URLconf
        1. Import the include() function: from django.urls import include, path
        2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

References
----------
    For more information please see:
        ``https://docs.djangoproject.com/en/2.0/topics/http/urls/``

Notes
-----
    Be aware that when a url is requested, it will be directed to the
    first matching path in the ``urlpatterns`` list that it finds. The
    ``<str:var>`` tag is just a placeholder. To avoid complications,
    users should order their paths in order from shortest to longest,
    and after that from most to least specific.
"""

from django.urls import path
from django.urls import re_path

from . import views

app_name = 'bespin_app'

urlpatterns = [

    # Home
    path('', views.home, name='home'),
    path('ajax/test_ec2/', views.test_ec2, name='test_ec2'),

]
