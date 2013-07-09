#!/usr/bin/env python

import xml.etree.ElementTree as ET
import sys
import crises.models as info

class BadXMLException(Exception):
    pass

def parseXML(file_chosen):
    '''
    toParse = "../xml/test.xml"
    
    if(len(file_chosen) > 0):
        toParse = file_chosen

    with open(toParse, 'r') as f:
    '''
    xmlInfo = file_chosen.readlines()

    # Disallow entities for now 
    # because we're using XSD
    for line in xmlInfo:
        if "!ENTITY" in line:
            raise BadXMLException("Bad XML File")
            
    tree = ET.fromstringlist(xmlInfo)
    return tree

def xmlToModels(eleTree):
    all_Information = []
    link_up_dict = {}
    crises_nodes = eleTree.findall("Crisis")
    all_Information = parseCrisis(crises_nodes[0],link_up_dict)
    return all_Information
    
def parseCrisis(crisis, lud):
    newCrisis = info.Crisis(id=crisis.attrib["ID"], name=crisis.attrib["Name"])
    #newCrisis.save()
    lud[newCrisis.id] = newCrisis
    return newCrisis
    
    

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
