"""KG URL Configuration

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
from Show_KG import views
urlpatterns = [
    url(r'^index/', views.index),
    url(r'^splash/',views.splash),
    url(r'^query_brother/',views.query_brother),
    url(r'^query_super/',views.query_super),
    url(r'^query_cooperation/',views.query_cooperation),
    url(r'^query_brother_page/', views.query_brother_page),
    url(r'^query_super_page/', views.query_super_page),
    url(r'^query_cooperation_page/', views.query_cooperation_page),
    url(r'^re_page/',views.re_page),
    url(r'^ner/',views.ner),
    url(r'^ner_page/',views.ner_page)
]
