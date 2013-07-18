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
    file_chosen = ''.join(x for x in file_cho)
    with open("WorldCrisis.xsd.xml", "r") as f:
        xsd = ''.join(x for x in f.readlines())
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
    reference_dict = {}
    
    crises_nodes = eleTree.findall("Crisis")
    people_nodes = eleTree.findall("Person")
    organization_nodes = eleTree.findall("Organization")
    
    #Must be parsed in this order due to dependencies :/ Sorry
    
    for person in people_nodes:
        temp = parsePerson(person,link_up_dict)
        all_Information  += (temp,)
        reference_dict[temp.id] = temp
    
    for organization in organization_nodes:
        temp = parseOrganization(organization,link_up_dict)
        all_Information  += (temp,)
        reference_dict[temp.id] = temp
    
    for problem in crises_nodes:
        temp = parseCrisis(problem,link_up_dict)
        all_Information  += (temp,)
        reference_dict[temp.id] = temp
    
    linkUpModels(reference_dict, link_up_dict)
    
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
    
    """
    #Parse the people
    if crisis.find("People") is not None:
        for person in crisis.find("People"):
            try:
                newCrisis.people.add(lud[person.attrib["ID"]])
            except:
                pass
        
    #Parse the organizations
    if crisis.find("Organizations") is not None:
        for organization in crisis.find("Organizations"):
            try:
                newCrisis.organizations.add(lud[organization.attrib["ID"]])
            except KeyError:
                pass
    """
    
    if newCrisis.id not in lud.keys():
        lud[newCrisis.id] = []
    
    if crisis.find("People") is not None:
        for person in crisis.find("People"):
            lud[newCrisis.id] += (person.attrib["ID"],)
            
    if crisis.find("Organizations") is not None:
        for organization in crisis.find("Organizations"):
            lud[newCrisis.id] += (organization.attrib["ID"],)
    
    
    #Parse the list types unique to crisis
    listElemDict = {}
    for val in info.CrisisListType.LIST_TYPE_CHOICES:
        listElemDict[val[1]] = val[0]
    
    for node in listElemDict.keys():
        if crisis.find(node) is not None:
            for i in crisis.find(node):
                parseListType(listElemDict[node], i, newCrisis)

    newCrisis.save()
    return newCrisis

def parsePerson(person, lud):
    newPerson = info.Person(id=person.attrib["ID"], name=person.attrib["Name"])
    newPerson.kind = person.find("Kind").text if person.find("Kind") is not None else ""
    newPerson.location = person.find("Location").text if person.find("Location") is not None else ""
    
    if person.find("Crises") is not None:
        for crisis in person.find("Crises"):
            if crisis.attrib["ID"] not in lud.keys():
                lud[crisis.attrib["ID"]] = []
            lud[crisis.attrib["ID"]] += (newPerson.id,)
    
    if person.find("Organizations") is not None:
        for org in person.find("Organizations"):
            if org.attrib["ID"] not in lud.keys():
                lud[org.attrib["ID"]] = []
            lud[org.attrib["ID"]] += (newPerson.id,)
    
    parseCommon(person.find("Common"), newPerson)
    newPerson.save()
    return newPerson

def parseOrganization(organization, lud):
    newOrg = info.Organization(id=organization.attrib["ID"], name=organization.attrib["Name"])
    newOrg.kind = organization.find("Kind").text if organization.find("Kind") is not None else ""
    newOrg.location = organization.find("Location").text if organization.find("Location") is not None else ""
    
    
    #Parse the common types
    parseCommon(organization.find("Common"), newOrg)
    newOrg.save()
    
    """
    #Old way of parsing. Flawed in the case where Person refers to Organization
    #Parse the People
    if organization.find("People") is not None:
        for person in organization.find("People"):
            try:
                newOrg.people.add(lud[person.attrib["ID"]])
            except KeyError:
                pass
    """
    
    if organization.find("People") is not None:
        for person in organization.find("People"):
           lud[newOrg.id] += (person.attrib["ID"],)
    
    if organization.find("Crises") is not None:
        for crisis in organization.find("Crises"):
            if crisis.attrib["ID"] not in lud.keys():
                lud[crisis.attrib["ID"]] = []
            lud[crisis.attrib["ID"]] += (newOrg.id,)
           
    #Iterates over History Types and parses them
    listElemDict = {}
    for val in info.OrganizationListType.LIST_TYPE_CHOICES:
        listElemDict[val[1]] = val[0]
    
    for node in listElemDict.keys():
        if organization.find(node) is not None:
            for i in organization.find(node):
                parseListType(listElemDict[node], i, newOrg)
        
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
    
def linkUpModels(references, links):
    for key in links.keys():
        model = references[key]
        for ID in links[key]:
            if ID.startswith("PER"):
                model.people.add(references[ID])
            else:
                model.organizations.add(references[ID])
            #print "LINKED", key, "WITH", ID
            #print
        model.save()
        
    

    

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
