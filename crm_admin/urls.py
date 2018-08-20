"""school_crm URL Configuration

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
from . import views

urlpatterns = [
    url('register', views.register, name='register'),
    url('login', views.user_login, name='login'),
    url('logout', views.user_logout, name='logout'),
    url('settings', views.user_settings, name='settings'),
    url('index', views.index, name='index'),
    url('(\w+)/(\w+)/(\d+)/change$', views.object_change),
    url('(\w+)/(\w+)/(\d+)/change/password$', views.password_change, name='password_change'),
    url('(\w+)/(\w+)/(\d+)/delete$', views.object_delete, name='object_delete'),
    url('(\w+)/(\w+)/add$', views.object_add),
    url('(\w+)/(\w+)$', views.show_tables, name='show_tables'),

]
