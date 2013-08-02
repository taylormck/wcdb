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

    # List pages,
    url(r'^crisis/$', views.listCrises, name='listCrises'),
    url(r'^organization/$', views.listOrganizations, name='listOrganizations'),
    url(r'^person/$', views.listPeople, name='listPeople'),

    # Dynamic pages
    # This is where we present the most of our data
    url(r'^crisis/(\w*)/$', views.crisis, name='crisis'),
    url(r'^organization/(\w*)/$', views.organization, name='organization'),
    url(r'^person/(\w*)/$', views.person, name='person'),
    
    # User pages for user profiles
    url(r'createuser/$', 'views.createuser', name = 'createuser'),
    url(r'login/$', 'views.login_user', name = 'loginuser'),

    # Search page
    url(r'^search/$', views.search, name='search'),

    # Import/Export pages
    url(r'^import/$', 'views.importScript', name='importScript'),
    url(r'^export/$', 'views.exportScript', name='exportScript'),

    # Test page
    url(r'^test/$', 'views.unittest', name='unittest'),

    # Log in page before import
    url(r'^password_required/$', 'password_required.views.login'),

    # About us page
    url(r'^about/$', 'views.about', name='about'),

    # queries page
    url(r'^queries/$', 'views.queries', name='queries'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    # Four oh four page
    # MUST BE LAST
    url(r'^.*/$', views.fourohfour, name='fourohfour'),
)
