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
    #TODO: WRITE THIS METHOD
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
    people_nodes = eleTree.findall("Person")
    organization_nodes = eleTree.findall("Organization")
    
    #Must be parsed in this order due to dependencies :/ Sorry
    
    for person in people_nodes:
        all_Information  += (parsePerson(person,link_up_dict),)
    
    for organization in organization_nodes:
        all_Information  += (parseOrganization(organization,link_up_dict),)
    
    for problem in crises_nodes:
        all_Information += (parseCrisis(problem,link_up_dict),)
    
    
    return (all_Information, ET.tostring(eleTree))

# ===================================
#      v   HERE BE PARSERS     v
# ===================================

def parseCrisis(crisis, lud):
    #Add all the basic info
    newCrisis = info.Crisis(id=crisis.attrib["ID"], name=crisis.attrib["Name"])
    
    newCrisis.date = date.parse(crisis.find("Date").text) if crisis.find("Date") is not None else None
    newCrisis.time = date.parse(crisis.find("Time").text) if crisis.find("Time") is not None else None
    newCrisis.kind = crisis.find("Kind").text if crisis.find("Kind") is not None else ""
    
    #Parse the common types
    parseCommon(crisis.find("Common"), newCrisis)
    newCrisis.save()
    
    #Parse the people
    for person in crisis.find("People"):
        newCrisis.people.add(lud[person.attrib["ID"]])
        
    #Parse the organizations
    for organization in crisis.find("Organizations"):
        newCrisis.organizations.add(lud[organization.attrib["ID"]])
    
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
        
    lud[newCrisis.id] = newCrisis
    newCrisis.save()
    return newCrisis
    '''
    person = info.Person(id='PER_TESTNO', name="NAME")
    person.save()
    newCrisis.save()
    newCrisis.people.add(person)
    newCrisis.save()
    return newCrisis
    '''

def parsePerson(person, lud):
    newPerson = info.Person(id=person.attrib["ID"], name=person.attrib["Name"])
    newPerson.kind = person.find("Kind").text if person.find("Kind") is not None else ""
    newPerson.location = person.find("Location").text if person.find("Location") is not None else ""
    
    parseCommon(person.find("Common"), newPerson)
    lud[newPerson.id] = newPerson
    newPerson.save()
    return newPerson

def parseOrganization(organization, lud):
    newOrg = info.Organization(id=organization.attrib["ID"], name=organization.attrib["Name"])
    newOrg.kind = organization.find("Kind").text if organization.find("Kind") is not None else ""
    newOrg.location = organization.find("Location").text if organization.find("Location") is not None else ""
    
    
    #Parse the common types
    parseCommon(organization.find("Common"), newOrg)
    newOrg.save()
    
    #Parse the People
    for person in organization.find("People"):
        newOrg.people.add(lud[person.attrib["ID"]])
    
    for i in organization.find("History"):
        parseListType(info.OrganizationListType.HISTORY, i, newOrg)
        
    for i in organization.find("ContactInfo"):
        parseListType(info.OrganizationListType.CONTACT_INFO, i, newOrg)
        
    lud[newOrg.id] = newOrg
    newOrg.save()
    return newOrg

def parseCommon(common, parentModel):
    if common is None:
        return
    
    container = info.Common()
    container.save()
    container.summary = common.find("Summary").text if common.find("Summary") is not None else ""
    
    for i in common.find("Citations"):
        parseListType(info.CommonListType.CITATIONS, i, container)
        
    for i in common.find("ExternalLinks"):
        parseListType(info.CommonListType.EXTERNAL_LINKS, i, container)
    
    for i in common.find("Images"):
        parseListType(info.CommonListType.IMAGES, i, container)
    
    for i in common.find("Videos"):
        parseListType(info.CommonListType.VIDEOS, i, container)
    
    for i in common.find("Maps"):
        parseListType(info.CommonListType.MAPS, i, container)
        
    for i in common.find("Feeds"):
        parseListType(info.CommonListType.FEEDS, i, container)
    
    parentModel.common_id = container.id
    container.save()

def parseListType(listType, node, parentModel):

    if type(parentModel) is info.Crisis:
        listMember = info.CrisisListType()
    elif type(parentModel) is info.Organization:
        listMember = info.OrganizationListType()
    else:
        listMember = info.CommonListType()
    
    try:
        listMember.href = node.attrib["href"]
    except KeyError:
        listMember.href = ""
    
    try:
        listMember.embed = node.attrib["embed"]
    except KeyError:
        listMember.embed = ""
        
    try:
        listMember.altText = node.attrib["text"]
    except KeyError:
        listMember.altText = ""
        
    listMember.text = node.text if node.text is not None else ""    
    listMember.context = listType
    listMember.owner_id = parentModel.id
    listMember.save()
    

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
