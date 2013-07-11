from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context, RequestContext, Template, loader
import scripts.imported as IMP
import sys

class Empty():
    pass

def index(request):
    html = open("static/html/index.html", 'r')
    
    return HttpResponse(html)


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
    html = open("static/html/bootstrapTest.html", 'r')
    # x = ''.join(line for line in html.readlines())        
    # t = Template(x)
    # c = RequestContext(request)
    # return HttpResponse(t.render(c))
    return HttpResponse(html)

def person1(request):
    html = open("static/html/person1.html", 'r')
    return HttpResponse(html)

def person2(request):
    html = open("static/html/person2.html", 'r')
    return HttpResponse(html)

def person3(request):
    html = open("static/html/person3.html", 'r')
    return HttpResponse(html)

def crisis1(request):
    html = open("static/html/crisis1.html", 'r')
    return HttpResponse(html)

def crisis2(request):
    html = open("static/html/crisis2.html", 'r')
    return HttpResponse(html)

def crisis3(request):
    html = open("static/html/crisis3.html", 'r')
    return HttpResponse(html)

def organization1(request):
    html = open("static/html/organization1.html", 'r')
    return HttpResponse(html)

def organization2(request):
    html = open("static/html/organization2.html", 'r')
    return HttpResponse(html)

def organization3(request):
    html = open("static/html/organization3.html", 'r')
    return HttpResponse(html)
