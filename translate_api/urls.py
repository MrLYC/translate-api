from django.conf.urls import patterns, include, url
from django.contrib import admin

from translate_api.views import post

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'translate_api.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^api/?', post),
)
