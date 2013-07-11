from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

import crises

urlpatterns = patterns('',
    #url(r'^crises/$', 'crises.test.current_datetime', name='house')

    #Index page
    url(r'^$', 'views.index', name='index'),
    url(r'base/$', 'views.base'), # template ?

    # Bootstrap test
    url(r'bootstrapTest/$', 'views.bootstrapTest'),

    # Static pages
    url(r'crisis1/$', 'views.crisis1', name='crisis1'),
    url(r'crisis2/$', 'views.crisis2', name='crisis2'),
    url(r'crisis3/$', 'views.crisis3', name='crisis3'),
    url(r'person1/$', 'views.person1', name='person1'),
    url(r'person2/$', 'views.person2', name='person2'),
    url(r'person3/$', 'views.person3', name='person3'),
    url(r'organization1/$', 'views.organization1', name='organization1'),
    url(r'organization2/$', 'views.organization2', name='organization2'),
    url(r'organization3/$', 'views.organization3', name='organization3'),
    
    # Import/Expert pages
    url(r'^import/$', 'views.importScript', name='importScript'),
    url(r'^export/$', 'views.exportScript', name='exportScript')
    
    # Examples:
    # url(r'^$', 'wcdb.views.home', name='home'),
    # url(r'^wcdb/', include('wcdb.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
