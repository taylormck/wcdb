from django.http import HttpResponse
from django import forms
from django.shortcuts import render_to_response
from django.template import Context, RequestContext, Template, loader
from django.contrib.auth.models import User
from password_required.decorators import password_required
import scripts.importScript as IMP
import scripts.export as EXP
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
from django.shortcuts import render
from models import LoginForm

import sys

class Empty():
    pass

def index(request):
    t = loader.get_template("index.html")
    return HttpResponse(t.render(RequestContext(request)))


def base(request):
    t = loader.get_template("base.html")
    c = RequestContext(request)
    return HttpResponse(t.render(c))
    #return render_to_response("static/html/base.html",
    #                          {},
    #                          context_instance=RequestContext(request))

@password_required
def importScript(request):
    information = {}
    if request.method == 'POST':
        try:
            xml = IMP.parseXML(request.FILES['xmlFile'])
            data = IMP.xmlToModels(xml)
            information = {"tree" : [data[0], data[1]]}
        except KeyError:
            pass
        except IMP.BadXMLException:
            information = {"tree" : "Upload Failed - Bad XML File!"}
        except IMP.ValdiationFailedException:
            information = {"tree" : "Upload Failed - Invalid XML File!"}
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
    # prettyXML = parseString(rawXML).toprettyxml()
    # prettyXML = html_decode(prettyXML)
    t = loader.get_template("export.xml")
    information = {"XML" : rawXML}
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

def login(request):
     t = loader.get_template("organization3.html")
     if request.method == 'POST': # If the form has been submitted...
        form = LoginForm(request.POST) # A form bound to the POST data
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
        form = LoginForm() # An unbound form

     return render(request, 'Login.html', {
        'form': form,})
