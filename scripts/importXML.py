#!/usr/bin/env python

import xml.etree.ElementTree as ET
import sys
import crises.models as info
import datetime
import dateutil.parser as date
import StringIO
from django.db.models.base import ObjectDoesNotExist

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
        
changes = False

def xmlToModels(eleTree):
    global changes
    changes = False
    link_up_dict = {}
    reference_dict = {}
    
    parseCrises(eleTree, reference_dict, link_up_dict)
    parsePeople(eleTree, reference_dict, link_up_dict)
    parseOrgs(eleTree, reference_dict, link_up_dict)
    
    linkUpModels(reference_dict, link_up_dict)
    eTree = ET.tostring(eleTree)
    returnMessage = "Database already contains all that information! No changes were made."
    
    if changes:
        returnMessage = "Success!"
        
    return returnMessage


def parseCrises(tree, ref,lud):
    parseGeneric(tree.findall("Crisis"), parseCrisis, ref, lud)

def parseOrgs(tree, ref,lud):
    parseGeneric(tree.findall("Person"), parsePerson, ref, lud)

def parsePeople(tree, ref,lud):
    parseGeneric(tree.findall("Organization"), parseOrganization, ref, lud)

def parseGeneric(nodes,parseFunction,ref,lud):
    for node in nodes:
        temp = parseFunction(node)
        addReferences(node,lud)
        ref[temp.id] = temp

# ===================================
#      v   HERE BE PARSERS     v
# ===================================

def parseCrisis(crisis):
    try:
        return info.Crisis.objects.get(id=crisis.attrib["ID"])
    except ObjectDoesNotExist:
        global changes
        changes = True
        
    #Add all the basic info
    newCrisis = info.Crisis(id=crisis.attrib["ID"], name=crisis.attrib["Name"])
    
    newCrisis.date = date.parse(crisis.find("Date").text) if crisis.find("Date") is not None else None
    newCrisis.time = date.parse(crisis.find("Time").text) if crisis.find("Time") is not None else None
    newCrisis.kind = crisis.find("Kind").text if crisis.find("Kind") is not None else ""
    
    #Parse the common types
    parseCommon(crisis.find("Common"), newCrisis)
    newCrisis.save()    
    
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

def parsePerson(person):
    try:
        return info.Person.objects.get(id=person.attrib["ID"])
    except ObjectDoesNotExist:
        global changes
        changes = True
        
    newPerson = info.Person(id=person.attrib["ID"], name=person.attrib["Name"])
    newPerson.kind = person.find("Kind").text if person.find("Kind") is not None else ""
    newPerson.location = person.find("Location").text if person.find("Location") is not None else ""
    
    parseCommon(person.find("Common"), newPerson)
    newPerson.save()
    return newPerson

def parseOrganization(organization):
    try:
        return info.Organization.objects.get(id=organization.attrib["ID"])
    except ObjectDoesNotExist:
        global changes
        changes = True
        
    newOrg = info.Organization(id=organization.attrib["ID"], name=organization.attrib["Name"])
    newOrg.kind = organization.find("Kind").text if organization.find("Kind") is not None else ""
    newOrg.location = organization.find("Location").text if organization.find("Location") is not None else ""
    
    
    #Parse the common types
    parseCommon(organization.find("Common"), newOrg)
    newOrg.save()
    
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
    _merge = True
    
    if type(parentModel) is info.Crisis:
        listType = info.CrisisListType
    elif type(parentModel) is info.Organization:
        listType = info.OrganizationListType
    else:
        listType = info.CommonListType
    
    listMember = listType()
    
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
    
    if _merge:
        commonObjects = listType.objects.filter(owner__exact=parentModel.id)
        hrefMatches = commonObjects.filter(href__exact=listMember.href).count()
        embedMatches = commonObjects.filter(embed__exact=listMember.embed).count()
        obj = None
        
        if (listMember.href != "" and hrefMatches):
            obj = commonObjects.filter(href__exact=listMember.href)[0]
        elif (listMember.href != "" and embedMatches):
            obj = commonObjects.filter(embed__exact=listMember.embed)[0]
        
        if obj is not None:
            listMember.id = obj.id
        
    
    listMember.text = node.text if node.text is not None else ""    
    listMember.context = listType
    listMember.owner_id = parentModel.id
    listMember.save()

#Basically, sets up our link up dictionary so we can do the DB relations properly
#owner_of_mtm = The model that owns the Many To Many objects
#subject_of_mtm = The owner of this model's many to many relation
def addReferences(node, ref):
    ID = node.attrib["ID"]
    
    if ID.startswith("CRI"):
        if ID not in ref.keys():
            ref[ID] = []
        
        owner_of_mtm = ["People", "Organizations"]
        subject_of_mtm = []
        
        
    elif ID.startswith("ORG"):
        if ID not in ref.keys():
            ref[ID] = []
        
        owner_of_mtm = ["People"]
        subject_of_mtm = ["Crises"]
        
    else:
        owner_of_mtm = []
        subject_of_mtm = ["Crises", "Organizations"]
    
    for choice in owner_of_mtm:
            if node.find(choice) is not None:
                for child in node.find(choice):
                    ref[ID] += (child.attrib["ID"],)
       
    for choice in subject_of_mtm:
        if node.find(choice) is not None:
            for child in node.find(choice):
                if child.attrib["ID"] not in ref.keys():
                    ref[child.attrib["ID"]] = []
                ref[child.attrib["ID"]] += (ID,)
    
    
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
