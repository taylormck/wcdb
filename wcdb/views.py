from django.http import HttpResponse

def index(request):
    html = open("index.html", 'r')
    return HttpResponse(html)