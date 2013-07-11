from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context, RequestContext, Template, loader
import scripts.imported as IMP
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

def imports(request):
    information = {}
    if request.method == 'POST':
        try:
            xml = IMP.parseXML(request.FILES['xmlFile'])
            data = IMP.xmlToModels(xml)
            information = {"tree" : [data[0], data[1]]}
        except KeyError:
            pass
        except IMP.BadXMLException:
            information = {"tree" : "Upload Failed!"}
    return render_to_response("import.html", information, context_instance=RequestContext(request))
    

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
