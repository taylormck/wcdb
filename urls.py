from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

import crises

urlpatterns = patterns('',
    url(r'^home.html', 'test.current_datetime', name='home'),
    #url(r'^crises/$', 'crises.test.current_datetime', name='house')
    (r'^world/$', 'crises.test.current_datetime'),

    #Index page
    (r'^$', 'views.index'),
    (r'base/$', 'views.base'),

    # Bootstrap test
    (r'bootstrapTest/$', 'views.bootstrapTest'),

    # Static pages
    (r'crisis1/$', 'views.crisis1'),
    (r'crisis2/$', 'views.crisis2'),
    (r'crisis3/$', 'views.crisis3'),
    (r'person1/$', 'views.person1'),
    (r'person2/$', 'views.person2'),
    (r'person3/$', 'views.person3'),
    (r'organization1/$', 'views.organization1'),
    (r'organization2/$', 'views.organization2'),
    (r'organization3/$', 'views.organization3'),

    # Examples:
    # url(r'^$', 'wcdb.views.home', name='home'),
    # url(r'^wcdb/', include('wcdb.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
