"""contact_book URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include

from contact_book import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^contact/(?P<id>\w+)/$', views.get_or_update_contact, name='get-or-update-contact'),
    url(r'^contact/$', views.create_contact, name='create-contact'),
    url(r'^contact/search$', views.search_contact, name='contact-list'),
]
