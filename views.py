from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context, RequestContext, Template

def index(request):
    html = open("static/html/index.html", 'r')
    return HttpResponse(html)


def base(request):
    html = open("static/html/base.html", 'r')
    x = ''.join(line for line in html.readlines())        
    t = Template(x)
    c = RequestContext(request)
    return HttpResponse(t.render(c))
    #return render_to_response('base.html',
    #                          {},
    #                          context_instance=RequestContext(request))
