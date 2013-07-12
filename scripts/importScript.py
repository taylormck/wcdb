#!/usr/bin/env python

import xml.etree.ElementTree as ET
import sys
import crises.models as info
import datetime
import dateutil.parser as date
import StringIO

from genxmlif import GenXmlIfError
from minixsv import pyxsval 

class BadXMLException(Exception):
    pass

class ValdiationFailedException(Exception):
    pass

def validateXML(file_cho):
    #TODO: WRITE THIS METHOD
    
    #STILL BROKEN the file needs to be  string thats the name of a file I believe 
    #Documentation for method http://www.leuthe-net.de/MiniXsv.html scroll down and see the method 
    file_chosen = ''.join(x for x in file_cho)
    with open("WorldCrisis.xsd.xml", "r") as f:
        xsd = ''.join(x for x in f.readlines())
    #Might need to move WordlCrisis.xsd.xml into scripts but I believe it worked last night in the wcdb folder
    try:
        pyxsval.parseAndValidateXmlInputString(file_chosen, xsdText=xsd, validateSchema=0)
   #if XML file did not follow the schema 
    except pyxsval.XsvalError, errstr:
        return False
   #if a parsing error
    except GenXmlIfError, errstr:
        return False

    return True

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
    
    if not validateXML(xmlInfo):
        raise ValdiationFailedException()

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
    if crisis.find("People") is not None:
        for person in crisis.find("People"):
            newCrisis.people.add(lud[person.attrib["ID"]])
        
    #Parse the organizations
    if crisis.find("Organizations") is not None:
        for organization in crisis.find("Organizations"):
            newCrisis.organizations.add(lud[organization.attrib["ID"]])
    
    #Parse the list types unique to crisis
    listElemDict = {}
    for val in info.CrisisListType.LIST_TYPE_CHOICES:
        listElemDict[val[1]] = val[0]
    
    for node in listElemDict.keys():
        if crisis.find(node) is not None:
            for i in crisis.find(node):
                parseListType(listElemDict[node], i, newCrisis)

    lud[newCrisis.id] = newCrisis
    newCrisis.save()
    return newCrisis

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
    if organization.find("People") is not None:
        for person in organization.find("People"):
            newOrg.people.add(lud[person.attrib["ID"]])
    
    #Iterates over History Types and parses them
    listElemDict = {}
    for val in info.OrganizationListType.LIST_TYPE_CHOICES:
        listElemDict[val[1]] = val[0]
    
    for node in listElemDict.keys():
        if organization.find(node) is not None:
            for i in organization.find(node):
                parseListType(listElemDict[node], i, newOrg)
        
    lud[newOrg.id] = newOrg
    newOrg.save()
    return newOrg

def parseCommon(common, parentModel):
    if common is None:
        return
    
    container = info.Common()
    container.save()
    container.summary = common.find("Summary").text if common.find("Summary") is not None else ""
    
    listElemDict = {}
    for val in info.CommonListType.LIST_TYPE_CHOICES:
        listElemDict[val[1]] = val[0]
    
    for node in listElemDict.keys():
        if common.find(node) is not None:
            for i in common.find(node):
                parseListType(listElemDict[node], i, container)
    
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
toParse = "../xml/tests.xml"

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
