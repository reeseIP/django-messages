"""
URL configuration for msgproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path, register_converter

#from django.apps import apps
from core.models import ExternalServices

urlpatterns = [
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
]

''' Service URL Patterns:
    A service url pattern is set using an apps config
        * the URL regex value will set by display_name
        * the included URLs are set by app_name
'''

services = [service.service for service in ExternalServices.objects.all()]

for service in services:
    urlpatterns.append(path(service+'/', include(service+'.urls')))
    urlpatterns.append(path(service.upper()+'/', include(service+'.urls')))
    urlpatterns.append(path(service.lower()+'/', include(service+'.urls')))

