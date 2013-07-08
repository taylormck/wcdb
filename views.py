from django.http import HttpResponse

def index(request):
    html = open("index.html", 'r')
    return HttpResponse(html)


def base(request):
    html = open("base.html", 'r')
    return HttpResponse(html)