from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context, RequestContext, Template, loader

def index(request):
    t = loader.get_template("index.html")
    return HttpResponse(t.render(RequestContext(request)))


def base(request):
    #html = open("static/html/base.html", 'r')
    t = loader.get_template("base.html")
    #t = Template(''.join(line for line in html.readlines()))
    c = RequestContext(request)
    return HttpResponse(t.render(c))
    #return render_to_response("static/html/base.html",
    #                          {},
    #                          context_instance=RequestContext(request))

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
