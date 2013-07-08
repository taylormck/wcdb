from django.http import HttpResponse

def index(request):
    html = open("static/html/index.html", 'r')
    return HttpResponse(html)


def base(request):
    html = open("static/html/base.html", 'r')
    return HttpResponse(html)
