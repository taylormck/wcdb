from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

import crises

urlpatterns = patterns('',
    url(r'^home.html', 'test.current_datetime', name='home'),
    #url(r'^crises/$', 'crises.test.current_datetime', name='house')
    (r'^world/$', 'crises.test.current_datetime'),
    # Examples:
    # url(r'^$', 'wcdb.views.home', name='home'),
    # url(r'^wcdb/', include('wcdb.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
