from django.http import HttpResponse
from django import forms
from django.shortcuts import render_to_response
from django.template import Context, RequestContext, Template, loader
from django.forms.models import model_to_dict # convert model to dict
from django.db.models.base import ObjectDoesNotExist

import crises.models as cm

from django.contrib.auth.models import User
from password_required.decorators import password_required
import scripts.importScript as IMP
import scripts.export as EXP
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
from django.shortcuts import render
from models import CreateUser

import sys


# Returns a dictionary containing the necessary
# additions to context
def getBaseContext():
    return {
        'dcrises' : cm.Crisis.objects.order_by('-date', '-time')[:10],
        'dorganizations' : cm.Organization.objects.order_by('name')[:10],
        'dpeople' : cm.Person.objects.order_by('name')[:10]
    }

# Helper functions to get tables as context
def getCrises():
    return {'crises' : cm.Crisis.objects.order_by('-date', '-time')}

def getOrganizations():
    return {'organizations' : cm.Organization.objects.order_by('name')}

def getPeople():
    return {'people' : cm.Person.objects.order_by('name')}



class Empty():
    pass

def index(request):
    t = loader.get_template("index.html")
    c = RequestContext(request, getBaseContext())
    return HttpResponse(t.render(c))

@password_required
def importScript(request):
    information = getBaseContext()
    if request.method == 'POST':
        try:
            xml = IMP.parseXML(request.FILES['xmlFile'])
            data = IMP.xmlToModels(xml)
            information = dict({"tree" : data}, **information)
        except KeyError:
            pass
        except IMP.BadXMLException:
            information = dict({"tree" : "Upload Failed - Bad XML File!"}, **information)
        except IMP.ValdiationFailedException:
            information = dict({"tree" : "Upload Failed - Invalid XML File!"}, **information)
    return render_to_response("import.html", information, context_instance=RequestContext(request))
    
    
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
    
def exportScript(request):
    rawXML = ET.tostring(EXP.exportXML())
    t = loader.get_template("export.xml")
    information = dict({"XML" : rawXML}, **getBaseContext())
    c = RequestContext(request, information)
    return HttpResponse(html_decode(t.render(c)), content_type="text/xml")
    
def bootstrapTest(request):
    t = loader.get_template("bootstrapTest.html")
    return HttpResponse(t.render(RequestContext(request)))

def person1(request):
    t = loader.get_template("person1.html")
    return HttpResponse(t.render(RequestContext(request)))

def person2(request):
    t = loader.get_template("person2.html")
    return HttpResponse(t.render(RequestContext(request)))

def person3(request):
    t = loader.get_template("person3.html")
    return HttpResponse(t.render(RequestContext(request)))

def crisis1(request):
    t = loader.get_template("crisis1.html")
    return HttpResponse(t.render(RequestContext(request)))

def crisis2(request):
    t = loader.get_template("crisis2.html")
    return HttpResponse(t.render(RequestContext(request)))

def crisis3(request):
    t = loader.get_template("crisis3.html")
    return HttpResponse(t.render(RequestContext(request)))

def organization1(request):
    t = loader.get_template("organization1.html")
    return HttpResponse(t.render(RequestContext(request)))

def organization2(request):
    t = loader.get_template("organization2.html")
    return HttpResponse(t.render(RequestContext(request)))

def organization3(request):
    t = loader.get_template("organization3.html")
    return HttpResponse(t.render(RequestContext(request)))

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
        c = RequestContext(request, addToContext)
        t = loader.get_template("crisis.html")
        return HttpResponse(t.render(c))
    except ObjectDoesNotExist:
        return fourohfour(request)

def organization(request, organization_id):
    try:
        thisOrganization = cm.Organization.objects.get(id=organization_id)
        addToContext = dict(model_to_dict(thisOrganization), **getBaseContext())
        c = RequestContext(request, addToContext)
        t = loader.get_template("organization.html")
        return HttpResponse(t.render(c))
    except ObjectDoesNotExist:
        return fourohfour(request)

def person(request, person_id):
    try:
        thisPerson = cm.Person.objects.get(id=person_id)
        addToContext = dict(model_to_dict(thisPerson), **getBaseContext())
        c = RequestContext(request, addToContext)
        t = loader.get_template("person.html")
        return HttpResponse(t.render(c))
    except ObjectDoesNotExist:
        return fourohfour(request)
      
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
            username = form.cleaned_data['username']
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            user = User.objects.create_user(username, email, password)
            user.last_name = lastname
            user.first_name = firstname
            user.save()
            return HttpResponse(t.render(RequestContext(request))) # Redirect after POST
     else:
        form = CreateUser() # An unbound form

     return render(request, 'CreateUser.html', {
        'form': form,})

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
