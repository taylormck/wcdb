#!/usr/bin/env python

import xml.etree.ElementTree as ET
import crises.models as info
import datetime

def exportXML():
    WorldCrises = ET.Element("WorldCrises")
    
    all_crises = info.Crisis.objects.all()
    all_people = info.Person.objects.all()
    all_organizations = info.Organization.objects.all()
    
    for crisis in all_crises:
        WorldCrises.append(createCrisisElement(crisis))
    
    for person in all_people:
        WorldCrises.append(createPersonElement(person))
        
    for organization in all_organizations:
        WorldCrises.append(createOrganizationElement(organization))
        
    return WorldCrises

def createCrisisElement(crisis):
    xmlCrisis = ET.Element("Crisis")
    
    xmlCrisis.attrib["ID"] = crisis.id
    xmlCrisis.attrib["Name"] = crisis.name
    
    get_all_elements(info.Person.objects, crisis, xmlCrisis, "Person")
    get_all_elements(info.Organization.objects, crisis, xmlCrisis, "Org")
    
    if crisis.kind != "":
        tag = ET.Element("Kind")
        tag.text = crisis.kind
        xmlCrisis.append(tag)
    
    if crisis.date is not None:
        tag = ET.Element("Date")
        tag.text = crisis.date.strftime("%Y-%m-%d")
        xmlCrisis.append(tag)
    
    if crisis.time is not None:
        tag = ET.Element("Time")
        tag.text = crisis.time.strftime("%H:%M:%S")
        xmlCrisis.append(tag)
    
    crisis_list_elems = info.CrisisListType.objects.filter(owner__exact=crisis.id)
    
    #Gets all the crisis types and adds them
    listElemDict = {}
    strict_order = []
    for val in info.CrisisListType.LIST_TYPE_CHOICES:
        listElemDict[val[0]] = ET.Element(val[1])
        strict_order += (val[0],)
    
    for element in crisis_list_elems:
        li = ET.Element("li")
        
        #Add all the relevant data
        if element.href != "":
            li.attrib["href"] = element.href
            
        if element.embed != "":
            li.attrib["embed"] = element.embed
        
        if element.altText != "":
            li.attrib["text"] = element.altText
        
        if element.text != "":
            li.text = element.text
        
        listElemDict[element.context].append(li)
        
    for val in strict_order:
        node = listElemDict[val]
        if len(node) > 0 or len(node.attrib) > 0 or node.text is not None:
            xmlCrisis.append(node)
            
    createCommonNode(crisis, xmlCrisis)
    
    return xmlCrisis
    
def createPersonElement(person):
    xmlPerson = ET.Element("Person")
    
    xmlPerson.attrib["ID"] = person.id
    xmlPerson.attrib["Name"] = person.name
    
    get_all_elements(info.Crisis.objects, person, xmlPerson, "Crisis")
    get_all_elements(info.Organization.objects, person, xmlPerson, "Org")
    
    if person.kind != "":
        tag = ET.Element("Kind")
        tag.text = person.kind
        xmlPerson.append(tag)
    
    if person.location != "":
        tag = ET.Element("Location")
        tag.text = person.location
        xmlPerson.append(tag)
        
    
    createCommonNode(person, xmlPerson)
    
    return xmlPerson

def createOrganizationElement(org):
    xmlOrg = ET.Element("Organization")
    
    xmlOrg.attrib["ID"] = org.id
    xmlOrg.attrib["Name"] = org.name
    
    get_all_elements(info.Crisis.objects, org, xmlOrg, "Crisis")
    get_all_elements(info.Person.objects, org, xmlOrg, "Person")
    
    if org.kind != "":
        tag = ET.Element("Kind")
        tag.text = org.kind
        xmlOrg.append(tag)
    
    if org.location != "":
        tag = ET.Element("Location")
        tag.text = org.location
        xmlOrg.append(tag)
        
    organization_list_elems = info.OrganizationListType.objects.filter(owner__exact=org.id)
    
    listElemDict = {}
    strict_order = []
    for val in info.OrganizationListType.LIST_TYPE_CHOICES:
        listElemDict[val[0]] = ET.Element(val[1])
        strict_order += (val[0],)
    
    for element in organization_list_elems:
        li = ET.Element("li")
        
        #Add all the relevant data
        if element.href != "":
            li.attrib["href"] = element.href
            
        if element.embed != "":
            li.attrib["embed"] = element.embed
        
        if element.altText != "":
            li.attrib["text"] = element.altText
        
        if element.text != "":
            li.text = element.text
        
        listElemDict[element.context].append(li)
        
    for val in strict_order:
        node = listElemDict[val]
        if len(node) > 0 or len(node.attrib) > 0 or node.text is not None:
            xmlOrg.append(node)
    
    createCommonNode(org, xmlOrg)
    
    return xmlOrg
    
#I apologize for this method - it's terrible
def get_all_elements(objects, filterID, parent, tagName):
    simpleDict = { "Crisis" : "Crises", "Org" : "Organizations", "Person" : "People"}
    
    if type(filterID) is info.Crisis:
        filterChoice = {"crisis__exact" : filterID}
    elif type(filterID) is info.Person:
        filterChoice = {"people__exact" : filterID}
    elif type(filterID) is info.Organization:
        if tagName == "Person":
            filterChoice = {"organization__exact" : filterID}
        else:
            filterChoice = {"organizations__exact" : filterID}
        
    xmlContainer = ET.Element(simpleDict[tagName])
    important_objects = objects.filter(**filterChoice)
    
    for obj in important_objects:
        objXml = ET.Element(tagName)
        objXml.attrib["ID"] = obj.id
        xmlContainer.append(objXml)
    
    if len(xmlContainer) > 0:    
        parent.append(xmlContainer)

def createCommonNode(owner, xmlNode):
    try:
        common = info.Common.objects.get(id=owner.common_id)
    except Exception:
        return
    xmlCommon = ET.Element("Common")
    common_list_elems = info.CommonListType.objects.filter(owner__exact=common.id)
    
    #Gets all the crisis types and adds them
    listElemDict = {}
    strict_order = []
    for val in info.CommonListType.LIST_TYPE_CHOICES:
        listElemDict[val[0]] = ET.Element(val[1])
        strict_order += (val[0],)
    
    for element in common_list_elems:
        li = ET.Element("li")
        
        #Add all the relevant data
        if element.href != "":
            li.attrib["href"] = element.href
            
        if element.embed != "":
            li.attrib["embed"] = element.embed
        
        if element.altText != "":
            li.attrib["text"] = element.altText
        
        if element.text != "":
            li.text = element.text
        
        listElemDict[element.context].append(li)
         
    for val in strict_order:
        node = listElemDict[val]
        if len(node) > 0 or len(node.attrib) > 0 or node.text is not None:
            xmlCommon.append(node)
        
    if common.summary != "":
        tag = ET.Element("Summary")
        tag.text = common.summary
        xmlCommon.append(tag)
        
    if len(xmlCommon) > 0:
        xmlNode.append(xmlCommon)
