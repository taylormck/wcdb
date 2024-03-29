from django.http import HttpResponse
from django import forms
from django.shortcuts import render_to_response
from django.template import Context, RequestContext, Template, loader
from django.forms.models import model_to_dict # convert model to dict
from django.db.models.base import ObjectDoesNotExist
from django.core.servers.basehttp import FileWrapper
from django.core.exceptions import *

import crises.models as cm

from django.contrib.auth.models import User
from password_required.decorators import password_required
import scripts.importXML as IMP
import scripts.exportXML as EXP
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
from xml.dom import minidom
from django.shortcuts import render
from models import *
from crispy_forms.helper import FormHelper
from django.contrib.auth import authenticate, login
import sys
import subprocess
import StringIO
import os
from random import choice

def getRandomCrisisID():
    allCrises = cm.Crisis.objects.all()
    numCrises = len(allCrises)
    if numCrises is 0:
        return {}
    else:
        return {'randomCrisis': choice(allCrises)}

# Returns a dictionary context for the navbar
def getBaseContext():
    return dict({
        'login_user': 'login_user',
        'dcrises' : cm.Crisis.objects.order_by('-date', '-time')[:10],
        'dorganizations' : cm.Organization.objects.order_by('?')[:10],
        'dpeople' : cm.Person.objects.order_by('?')[:10],
    }, **getRandomCrisisID())

# Helper functions to get tables as context
def getCrises():
    return {'crises' : cm.Crisis.objects.order_by('-date', '-time')}

def getOrganizations():
    return {'organizations' : cm.Organization.objects.order_by('name')}

def getPeople():
    return {'people' : cm.Person.objects.order_by('name')}

# Add common info to context
def getCommonContext(common_id):
    images = []
    links = []
    videos = []
    maps = []
    feeds = []

    for i in cm.CommonListType.objects.filter(owner__exact=common_id):
        if (i.context == cm.CommonListType.IMAGES):
            images += [(i.embed, i.altText)]
        elif (i.context == cm.CommonListType.EXTERNAL_LINKS):
            links += [(i.href, i.text)]
        elif (i.context == cm.CommonListType.VIDEOS):
            videos += [(i.href, i.text)]
        elif (i.context == cm.CommonListType.MAPS):
            videos += [(i.href, i.text)]
        # elif (i.context == cm.CommonListType.FEEDS):
        #     feeds += [(i.href, i.text)]

    return {
        'images' : images,
        'links' : links,
        'videos' : videos,
        'maps' : maps,
        'feeds' : feeds,
    }

# Get info for crises
def getCrisesContext(crisis_id):
    common = cm.Common.objects.get(crisis__id__exact=crisis_id)
    summaries = []
    if common.summary != "":
        summaries += [common.summary]

    locations = []
    humanImpact = []
    economicImpact = []
    resourcesNeeded = []
    waysToHelp = []
    orgs = []
    peeps = []

    for i in cm.CrisisListType.objects.filter(owner__exact=crisis_id):
        if(i.context == cm.CrisisListType.LOCATION):
            locations += [i.text]
        elif(i.context == cm.CrisisListType.HUMAN_IMPACT):
            humanImpact += [i.text]
        elif(i.context == cm.CrisisListType.ECONOMIC_IMPACT):
            economicImpact += [i.text]
        elif(i.context == cm.CrisisListType.RESOURCES_NEEDED):
            resourcesNeeded += [i.text]
        elif(i.context == cm.CrisisListType.WAYS_TO_HELP):
            waysToHelp += [i.text]

    for i in cm.Organization.objects.filter(crisis__id__exact=crisis_id):
        orgs += [i]

    for i in cm.Person.objects.filter(crisis__id__exact=crisis_id):
        peeps += [i]

    return {
        'summaries' : summaries,
        'locations' : locations,
        'humanImpact' : humanImpact,
        'economicImpact' : economicImpact,
        'resourcesNeeded' : resourcesNeeded,
        'waysToHelp' : waysToHelp,
        'orgs' : orgs,
        'peeps' : peeps,
    }

# Get context for organizations
def getOrganizationContext(organization_id):
    common = cm.Common.objects.get(organization__id__exact=organization_id)
    summaries = []
    if common.summary != "":
        summaries += [common.summary]

    history = []
    contactInfo = []
    peeps = []
    cries = []

    for i in cm.OrganizationListType.objects.filter(owner__exact=organization_id):
        if (i.context == cm.OrganizationListType.HISTORY):
            history += [i.text]
        elif (i.context == cm.OrganizationListType.CONTACT_INFO):
            contactInfo += [i.text]

    for i in cm.Person.objects.filter(organization__id__exact=organization_id):
        peeps += [i]

    for i in cm.Crisis.objects.filter(organizations__id__exact=organization_id):
        cries += [i]

    return {
        'summaries' : summaries,
        'history' : history,
        'contactInfo' : contactInfo,
        'peeps' : peeps,
        'cries' : cries,
    }

# Get context for organizations
def getPersonContext(person_id):
    common = cm.Common.objects.get(person__id__exact=person_id)
    summaries = []
    if common.summary != "":
        summaries += [common.summary]

    cries = []
    for i in cm.Crisis.objects.filter(people__id__exact=person_id):
        cries += [i]

    orgs = []
    for i in cm.Organization.objects.filter(people__id__exact=person_id):
        orgs += [i]

    return {
        'summaries' : summaries,
        'orgs' : orgs,
        'cries' : cries,
    }


class Empty():
    pass

def about(request):
    t = loader.get_template("about.html")
    c = RequestContext(request, getBaseContext())
    return HttpResponse(t.render(c))

def index(request):
    t = loader.get_template("index.html")
    c = RequestContext(request, getBaseContext())
    return HttpResponse(t.render(c))

@password_required
def importScript(request):
    information = {}
    if request.method == 'POST':
        oldMerge = IMP.setMerge("merge" in request.POST)
        try:
            xml = IMP.parseXML(request.FILES['xmlFile'])
            data = IMP.xmlToModels(xml)
            information = {"tree" : data}
        except KeyError:
            pass
        except IMP.BadXMLException:
            information = {"tree" : "Upload Failed - Bad XML File!"}
        except IMP.ValdiationFailedException:
            information = {"tree" : "Upload Failed - Invalid XML File!"}
        IMP.setMerge(oldMerge)
    information = dict(getBaseContext(), **information)
    t = loader.get_template("import.html")
    c = RequestContext(request, information)
    return HttpResponse(t.render(c))


def html_decode(s):
    """
    Returns the ASCII decoded version of the given HTML string. This does
    NOT remove normal HTML tags like <p>.
    """
    htmlCodes = (
            ("'", '&#39;'),
            ('"', '&quot;'),
            ('>', '&gt;'),
            ('<', '&lt;'),
            ('&', '&amp;')
        )
    for code in htmlCodes:
        s = s.replace(code[1], code[0])
    return s

def prettyXML(rawXML):
    jacked =  minidom.parseString(rawXML).toprettyxml()
    return '\n'.join(l for l in jacked.split('\n') if l.strip())

def exportScript(request):
    rawXML = ET.tostring(EXP.exportXML())

    export = StringIO.StringIO(prettyXML(rawXML))

    contentType = "text/wcdb1"

    response = HttpResponse(FileWrapper(export), content_type=contentType)
    response['Content-Disposition'] = 'attachment; filename=export.xml'

    return response

# List pages
def listCrises(request):
    addToContext = dict(getCrises(), **getBaseContext())
    c = RequestContext(request, addToContext)
    t = loader.get_template("listCrises.html")
    return HttpResponse(t.render(c))

def listOrganizations(request):
    addToContext = dict(getOrganizations(), **getBaseContext())
    c = RequestContext(request, addToContext)
    t = loader.get_template("listOrganization.html")
    return HttpResponse(t.render(c))

def listPeople(request):
    addToContext = dict(getPeople(), **getBaseContext())
    c = RequestContext(request, addToContext)
    t = loader.get_template("listPeople.html")
    return HttpResponse(t.render(c))

# Dynamic pages
def crisis(request, crisis_id):
    try:
        thisCrisis = cm.Crisis.objects.get(id=crisis_id)
        addToContext = dict({'crisis' : thisCrisis}, **getBaseContext())
        addToContext = dict(getCommonContext(thisCrisis.common_id), **addToContext)
        addToContext = dict(getCrisesContext(thisCrisis.id), **addToContext)
        c = RequestContext(request, addToContext)
        t = loader.get_template("crisis.html")
        return HttpResponse(t.render(c))
    except ObjectDoesNotExist:
        return fourohfour(request)

def organization(request, organization_id):
    try:
        thisOrganization = cm.Organization.objects.get(id=organization_id)
        addToContext = dict(model_to_dict(thisOrganization), **getBaseContext())
        addToContext = dict(getCommonContext(thisOrganization.common_id), **addToContext)
        addToContext = dict(getOrganizationContext(thisOrganization.id), **addToContext)
        c = RequestContext(request, addToContext)
        t = loader.get_template("organization.html")
        return HttpResponse(t.render(c))
    except ObjectDoesNotExist:
        return fourohfour(request)

def person(request, person_id):
    try:
        thisPerson = cm.Person.objects.get(id=person_id)
        addToContext = dict(model_to_dict(thisPerson), **getBaseContext())
        addToContext = dict(getCommonContext(thisPerson.common_id), **addToContext)
        addToContext = dict(getPersonContext(thisPerson.id), **addToContext)
        c = RequestContext(request, addToContext)
        t = loader.get_template("person.html")
        return HttpResponse(t.render(c))
    except ObjectDoesNotExist:
        return fourohfour(request)

#creating a user page

def createuser(request):
     t = loader.get_template("index.html")
     if request.method == 'POST': # If the form has been submitted...
        form = CreateUser(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            #firstname = form.cleaned_data['firstname']
            #lastname = form.cleaned_data['lastname']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            usern = form.cleaned_data['username']
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            adminpass = form.cleaned_data['admin']
            try:
                user = User.objects.get(username=usern)
                form._errors["username"] = form.error_class(["Username is already in use"])
                return render(request,
                   'createUser.html',
                   dict({'form': form,}, **getBaseContext()))
            except User.DoesNotExist:
                user = User.objects.create_user(usern, email, password)
                user.last_name = lastname
                user.first_name = firstname
                if adminpass == "downing" :
                    user.is_superuser = True
                user.save()
                user = authenticate(username=usern, password=password)
                login(request, user)
                c = RequestContext(request, getBaseContext())
                return HttpResponse(t.render(c)) # Redirect after POST
            else :
                form = CreateUser(0)
     else:
        form = CreateUser() # An unbound form

     return render(request,
                   'createUser.html',
                   dict({'form': form,}, **getBaseContext()))

#logining in a user
def login_user(request):
  t = loader.get_template("index.html")
  if request.method == 'POST':
    form = LoginUser(request.POST)
    if form.is_valid():
      username = form.cleaned_data['username']
      password = form.cleaned_data['password']
      user = authenticate(username=username, password=password)
      if user is not None:
        login(request, user)
        c = RequestContext(request, getBaseContext())
        return HttpResponse(t.render(c)) # Redirect after POST
      else :
        form._errors["password"] = form.error_class(["Username and password combination not valid"])
        form._errors["username"] = form.error_class(["Username and password combination not valid"])
        return render(request, 'Login.html', dict({'temp': form,}, **getBaseContext()))
  else:
    form = LoginUser() #unbound form

  return render(request, 'Login.html', dict({'temp': form,}, **getBaseContext()))

# Our four oh four page
def fourohfour(request):
    addToContext = getBaseContext()
    c = RequestContext(request, addToContext)
    t = loader.get_template("fourohfour.html")
    return HttpResponse(t.render(c))

# Our search page
def search(request):
    people = set([])
    organizations = set([])
    crises = set([])

    for i in request.GET.values():
        queries = i.split()
        for q in queries:
            people.update(cm.Person.objects.filter(name__icontains=q))
            organizations.update(cm.Organization.objects.filter(name__icontains=q))
            crises.update(cm.Crisis.objects.filter(name__icontains=q))

    addToContext = {
        'people' : people,
        'organizations' : organizations,
        'crises' : crises
    }
    addToContext = dict(getBaseContext(), **addToContext)
    c = RequestContext(request, addToContext)
    t = loader.get_template("search.html")
    return HttpResponse(t.render(c))

def unittest(request):
    text = StringIO.StringIO()
    copyout = sys.stdout
    sys.stdout = text

    try:
        print "TestWCDB1.py"
        print subprocess.check_output(["python", "manage.py", "test"], stderr=subprocess.STDOUT)
        print "Done."
    except subprocess.CalledProcessError as e:
        print e.output
        print "Done."


    addToContext = {
        'output' : text.getvalue()
    }
    sys.stdout = copyout
    text.close()
    addToContext = dict(getBaseContext(), **addToContext)
    c = RequestContext(request, addToContext)
    t = loader.get_template("unittest.html")
    return HttpResponse(t.render(c))

def queries(request):
    addToContext = getBaseContext()
    c = RequestContext(request, addToContext)
    t = loader.get_template("queries.html")
    return HttpResponse(t.render(c))
