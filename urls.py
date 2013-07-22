from django.conf.urls.defaults import *
import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

import crises

urlpatterns = patterns('',
    # Index page
    # TODO do something with the index page to make it more interesting
    url(r'^$', 'views.index', name='index'),

    # Static pages
    # TODO I'm leaving these for now so we can look at them,
    # but they should be deleted eventually
    url(r'crisis1/$', 'views.crisis1', name='crisis1'),
    url(r'crisis2/$', 'views.crisis2', name='crisis2'),
    url(r'crisis3/$', 'views.crisis3', name='crisis3'),
    url(r'person1/$', 'views.person1', name='person1'),
    url(r'person2/$', 'views.person2', name='person2'),
    url(r'person3/$', 'views.person3', name='person3'),
    url(r'organization1/$', 'views.organization1', name='organization1'),
    url(r'organization2/$', 'views.organization2', name='organization2'),
    url(r'organization3/$', 'views.organization3', name='organization3'),

    # List pages,
    url(r'^crisis/$', views.listCrises, name='listCrises'),
    url(r'^organization/$', views.listOrganizations, name='listOrganizations'),
    url(r'^person/$', views.listPeople, name='listPeople'),

    # Dynamic pages
    # This is where we present the most of our data
    url(r'^crisis/(\w*)/$', views.crisis, name='crisis'),
    url(r'^organization/(\w*)/$', views.organization, name='organization'),
    url(r'^person/(\w*)/$', views.person, name='person'),
    
    # Import/Export pages
    url(r'^import/$', 'views.importScript', name='importScript'),
    url(r'^export/$', 'views.exportScript', name='exportScript'),
    
    # Log in page before import
    url(r'^password_required/$', 'password_required.views.login'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    # Four oh four page
    # MUST BE LAST
    url(r'^.*/$', views.fourohfour, name='fourohfour'),
)
