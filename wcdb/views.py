from django.http import HttpResponse

def index(request):
    html = "<html><body>Woohoo !! Index page</body></html>"
    return HttpResponse(html)