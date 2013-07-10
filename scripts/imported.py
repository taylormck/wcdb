#!/usr/bin/env python

import xml.etree.ElementTree as ET
import sys
import crises.models as info
import datetime
import dateutil.parser as date

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
    #Add all the basic info
    newCrisis = info.Crisis(id=crisis.attrib["ID"], name=crisis.attrib["Name"])
    
    newCrisis.date = date.parse(crisis.find("Date").text) if crisis.find("Date") else None
    newCrisis.time = date.parse(crisis.find("Time").text) if crisis.find("Time") else None
    newCrisis.kind = crisis.find("Kind").text if crisis.find("Kind") else None
    
    #Parse the list types unique to crisis
    
    for i in crisis.find("Locations"):
        parseListType(info.CrisisListType.LOCATION, i, newCrisis)
        
    for i in crisis.find("HumanImpact"):
        parseListType(info.CrisisListType.HUMAN_IMPACT, i, newCrisis)
    
    for i in crisis.find("EconomicImpact"):
        parseListType(info.CrisisListType.ECONOMIC_IMPACT, i, newCrisis)
    
    for i in crisis.find("ResourcesNeeded"):
        parseListType(info.CrisisListType.RESOURCES_NEEDED, i, newCrisis)
    
    for i in crisis.find("WaysToHelp"):
        parseListType(info.CrisisListType.WAYS_TO_HELP, i, newCrisis)
        
    #Parse the common types
    
    parseCommon(crisis.find("Common"), newCrisis)
    
    lud[newCrisis.id] = newCrisis
    '''
    person = info.Person(id='PER_TESTNO', name="NAME")
    person.save()
    newCrisis.save()
    newCrisis.people.add(person)
    newCrisis.save()
    return newCrisis
    '''

def parsePerson(person, lud):
    pass

def parseOrganization(organization, lud):
    pass

def parseCommon(common, parentModel):
    if not common:
        return
    
    container = info.Common()
    
    for i in common.find("Citations"):
        parseListType(info.CommonListType.CITATIONS, i, newCrisis)
        
    for i in common.find("ExternalLinks"):
        parseListType(info.CommonListType.EXTERNAL_LINKS, i, newCrisis)
    
    for i in common.find("Images"):
        parseListType(info.CommonListType.IMAGES, i, newCrisis)
    
    for i in common.find("Videos"):
        parseListType(info.CommonListType.VIDEOS, i, newCrisis)
    
    for i in common.find("Maps"):
        parseListType(info.CommonListType.MAPS, i, newCrisis)
        
    for i in common.find("Feeds"):
        parseListType(info.CommonListType.FEEDS, i, newCrisis)
    
    container.summary = common.find("Summary").text if common.find("Summary") else ""

def parseListType(listType, node, parentModel):
    if type(parentModel) is info.Crisis:
        listMember = info.CrisisListType()
    else
        listMember = info.CommonListType()
    
    node = node.find("li")
    
    try:
        listMember.href = node.attrib["href"]
    except KeyError:
        listMember.href = ""
    
    try:
        listMember.embed = node.attrib["embed"]
    except KeyError:
        listMember.embed = ""
        
    try:
        listMember.altText = node.attrib["altText"]
    except KeyError:
        listMember.altText = ""
        
    listMember.text = node.text    
    listMember.context = listType    
    listMember.owner_id = parentModel.id
    

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
