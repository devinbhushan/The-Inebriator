from django.conf.urls.defaults import patterns, include, url
from search_engine.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Inebriator.views.home', name='home'),
    # url(r'^Inebriator/', include('Inebriator.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    (r'^$', home),
    (r'^home/', home),
    (r'^search/$', search),
    (r'^search/(?P<page>\d{1})/', search),
    (r'^trending/', trending),
    (r'^popular/', popular),
)
