"""poet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, patterns
from django.contrib import admin

from .views.hello import hello
from .views.home import home
from .views.member import (MemberList,
                           MemberView,
                           MemberCreate)

admin.autodiscover()

urlpatterns = patterns('',

    # Home page
     url(r'^$', home,
        name='home'),
    # Hello Test
    url(r'^hello', hello,
        name='poet_hello'),
    # PoetMember management
    url(r'^member/$', MemberList.as_view(),
                           name='member_list'),
    url(r'^member/(?P<slug>[-\w]+)/$', MemberView.as_view(),
                           name='member_view'),

    url(r'^member/create$', MemberCreate.as_view(),
                           name='member_create'),


    url(r'^_admin/', include(admin.site.urls)),

)
