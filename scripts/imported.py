#!/usr/bin/env python

import xml.etree.ElementTree as ET
import sys
import crises.models as info
import datetime

class BadXMLException(Exception):
    pass

class ValdiationFailedException(Exception):
    pass

def validateXML(file_chosen):
    return True

def parseXML(file_chosen):
    '''
    toParse = "../xml/test.xml"
    
    if(len(file_chosen) > 0):
        toParse = file_chosen

    with open(toParse, 'r') as f:
    '''
    
    if not validateXML(file_chosen):
        raise ValdiationFailedException()
    
    xmlInfo = file_chosen.readlines()

    # Disallow entities for now 
    # because we're using XSD
    for line in xmlInfo:
        if "!ENTITY" in line:
            raise BadXMLException("Bad XML File")
    try:
        tree = ET.fromstringlist(xmlInfo)
        return tree
    except Exception:
        raise BadXMLException("Parse Failed")

def xmlToModels(eleTree):
    all_Information = []
    link_up_dict = {}
    
    crises_nodes = eleTree.findall("Crisis")
    
    all_Information = parseCrisis(crises_nodes[0],link_up_dict)
    
    
    return all_Information
    
def parseCrisis(crisis, lud):
    newCrisis = info.Crisis(id=crisis.attrib["ID"], name=crisis.attrib["Name"])
    
    newCrisis.date = datetime.datetime.now()
    newCrisis.time = datetime.datetime.now()
    '''
    lud[newCrisis.id] = newCrisis
    person = info.Person(id='PER_TESTNO', name="NAME")
    person.save()
    newCrisis.save()
    newCrisis.people.add(person)
    newCrisis.save()
    return newCrisis

def parsePerson(person, lud):
    pass

def parseOrganization(organization, lud):
    pass

def parseCommon(common, parentModel):
    pass

    

"""
toParse = "../xml/test.xml"

if len(sys.argv) > 1:   
    toParse = sys.argv[1]


with open(toParse, 'r') as f:
    xmlInfo = f.readlines()

# Disallow entities for now 
# because we're using XSD
for line in xmlInfo:
    if "!ENTITY" in line:
        raise BadXMLException("Bad XML File")
        
tree = ET.fromstringlist(xmlInfo)

ET.dump(tree)
"""
