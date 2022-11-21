# coding=utf8; version=2013011202
from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout
from vvkws.views import *
from vvkws.forms import *

# Admin enable:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    ('^hello/$',hello),
    ('^ehllo/$',ehllo),
    ('^time/$',nowtm),
    ('^now/1/$',nowtpls1),
    ('^now/2/$',nowtpls2),
    (r'^time/plus/(\d{1,2})/$',hour_ahead),
    (r'^time/tpls/(\d{1,2})/$',hour_ahead_tpls1),
    ('^hosts/$',host_list),
    ('^books/$',book_list),
    ('^browser/$', get_browser),
    ('^meta/$', display_meta),
    ('^pdf1/$', hello_pdf),
    ('^pdf2/$', string_pdf),
    (r'^search-form/$', search_form),
    (r'^search/$', search),
    (r'^contact/$', contact),
    (r'^accounts/login/$', login),
    (r'^accounts/logout/$', logout),
    ('^login/$', login_view),
    ('^logout/$', logout_view),
    ('^register/$', register),
#   (r'^events/$', object_list, {'model': models.Event}),
#   (r'^blog/entries/$', object_list, {'model': BlogEntry}),
    # Examples:
    # url(r'^$', 'vvkws.views.home', name='home'),
    # url(r'^vvkws/', include('vvkws.foo.urls')),
    # Admin enable:
#   url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
#   url(r'^admin/', include(admin.site.urls)),
)
