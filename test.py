from django.http import HttpResponse
import datetime
import os
import xml.etree.ElementTree as ET

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)
    
print os.getcwd()

print "AHAHA" if None else "BABAB"

tree = ET.fromstring("<cats happy=\"whoooo\"></cats>")
print tree.attrib["happy"]
print tree.attrib["sad"]
