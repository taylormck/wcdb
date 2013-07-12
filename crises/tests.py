"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

We will definitely want to add many many more tests, but for now, 3 per
function will have to do.


"""
# --- imports ---
import StringIO
import xml.etree.ElementTree as et
from django.test import TestCase
from django.db.models.base import ObjectDoesNotExist
import crises.models as cm
from scripts.importScript import *
from scripts.export import *

NIFCrisis = """
    <Crisis ID="CRI_AURSHO" Name="2013 Northern India Floods">
        <Kind>Natural Disaster</Kind>
        <Date>2013-06-14</Date>
        <Time>00:00:00</Time>
        <Common>
            <Citations>
                <li>The Hindustan Times</li>
                <li>The Times of India</li>
            </Citations>
            <ExternalLinks>
                <li href="http://en.wikipedia.org/wiki/2013_North_India_floods">Wikipedia</li>
            </ExternalLinks>
            <Images>
                <li embed="http://images.jagran.com/ukhand-ss-02-07-13.jpg" text="This is the alt element of the image."/>
                <li embed="http://timesofindia.indiatimes.com/photo/15357310.cms"/>
            </Images>
            <Videos>
                <li embed="//www.youtube.com/embed/qV3s7Sa6B6w"/>
            </Videos>
            <Maps>
                <li embed="[fake]"/>
            </Maps>
            <Feeds>
                <li embed="[WHATEVER A FEED URL LOOKS LIKE]"/>
            </Feeds>
            <Summary>Lorem ipsum...</Summary>
        </Common>
    </Crisis>
"""

CFFOrg = """
    <Organization ID="ORG_COFIFO" Name="The Community First Foundation">
        <Crises>
            <Crisis ID="CRI_AURSHO"/>
        </Crises>
        <Kind>Charity</Kind>
        <Location>United States</Location>
        <History>
            <li>This is a story all about how...</li>
        </History>
    </Organization>
"""

JEHPerson = """
    <Person ID="PER_JAEAHO" Name="James Eagen Holmes">
        <Crises>
            <Crisis ID="CRI_AURSHO"/>
        </Crises>
        <Kind>Mass Murderer</Kind>
        <Location>Aurora, CO, USA</Location>
        <Common>
            <Summary>I have nothing nice to say about this man.</Summary>
        </Common>
    </Person>
"""

TestFile = "<WorldCrises>"+"\n"+ NIFCrisis +"\n"+ JEHPerson+"\n" +CFFOrg +"\n" + "</WorldCrises>"

class TestImportScript(TestCase):
    # TODO must make sure to make proper XML strings for these
    def test_parsevalidate_01(TestCase):
        assert validateXML(TestFile)
        
    def test_parsevalidate_02(TestCase):
        assert not validateXML(NIFCrisis)
        
    def test_parsevalidate_03(TestCase):
        testXML = StringIO.StringIO("<Dragon><Cooly></Cooly></Dragon>")
        assert not validateXML(testXML)
        
    def test_parseXML_01(self):
        testXML = StringIO.StringIO("<Dragon></Dragon>")
        try:
            root = parseXML(testXML)
            assert(False)
        except Exception:
            pass

    def test_parseXML_02(TestCase):
        testXML = StringIO.StringIO(TestFile)
        root = None
        try:
            parseXML(testXML)
            assert(False)
        except Exception:
            pass

    def test_parseXML_03(TestCase):
        testXML = StringIO.StringIO(TestFile)
        try:
            parseXML(testXML)
            assert(False)
        except Exception:
            pass

    def test_parseCrisis_01(TestCase):
        testElement = et.fromstring(NIFCrisis)
        testDict = {}
        testCrisis = parseCrisis(testElement, testDict)
        try:
            testCrisisCopy = cm.Crisis.objects.get(id="CRI_AURSHO")
        except ObjectDoesNotExist:
            assert(False)
        assert(testCrisis == testCrisisCopy)
        assert(testCrisis.name == "2013 Northern India Floods")

    def test_parseCrisis_02(TestCase):
        try:
            while True:
                testCrisisCopy = cm.Crisis.objects.get(id="CRI_AURSHO")
                testCrisisCopy.delete()
                assert(False)
        except ObjectDoesNotExist:
            pass
        
    def test_parseCrisis_03(TestCase):
        testElement = et.fromstring(NIFCrisis)
        testDict = {}
        testCrisis = parseCrisis(testElement, testDict)
        try:
            testCrisisCopy = cm.Crisis.objects.get(id="CRI_AURSH")
            assert(False)
        except ObjectDoesNotExist:
            pass
        
    def test_parseOrganization_01(TestCase):
        testElement = et.fromstring(CFFOrg)
        testDict = {}
        testOrg = parseOrganization(testElement, testDict)
        try:
            testOrgCopy = cm.Organization.objects.get(id="ORG_COFIFO")
        except ObjectDoesNotExist:
            assert(False)
        assert(testOrg == testOrgCopy)
        assert(testOrg.kind == "Charity")
        
    def test_parseOrganization_02(TestCase):
        testElement = et.fromstring(CFFOrg)
        testDict = {}
        parseOrganization(testElement, testDict)
        try:
            testOrgCopy = cm.Organization.objects.get(id="ORG_COFIFO")
        except ObjectDoesNotExist:
            assert(False)
        assert(testDict["ORG_COFIFO"] == testOrgCopy)
        
    def test_parseOrganization_03(TestCase):
        testElement = et.fromstring(CFFOrg)
        testDict = {}
        testOrg = parseOrganization(testElement, testDict)
        try:
            while True:
                testOrg.delete()
                testOrgCopy = cm.Organization.objects.get(id="CRI_COFIFO")
                assert(False)
        except ObjectDoesNotExist:
            pass
        
    def test_parsePerson_01(TestCase):
        testElement = et.fromstring(JEHPerson)
        testDict = {}
        testPer = parsePerson(testElement, testDict)
        try:
            testPerCopy = cm.Person.objects.get(id="PER_JAEAHO")
        except ObjectDoesNotExist:
            assert(False)
        assert(testPer == testPerCopy)
        assert(testPer.kind == "Mass Murderer")
        
    def test_parsePerson_02(TestCase):
        testElement = et.fromstring(JEHPerson)
        testDict = {}
        parsePerson(testElement, testDict)
        try:
            testPerCopy = cm.Person.objects.get(id="PER_JAEAHO")
        except ObjectDoesNotExist:
            assert(False)
        assert(testDict["PER_JAEAHO"] == testPerCopy)
        
    def test_parsePerson_03(TestCase):
        testElement = et.fromstring(JEHPerson)
        testDict = {}
        testPer = parsePerson(testElement, testDict)
        try:
            testPer.delete()
            testPerCopy = cm.Person.objects.get(id="PER_JAEAHO")
            assert(False)
        except ObjectDoesNotExist:
            pass

"""
class TestExportScript(TestCase):
    def test_everything(TestCase):
        testXML = StringIO.StringIO(TestFile)
        
        parse = parseXML(testXML)
        root = et.fromstring(TestFile)

        assert(et.tostring(parse) == et.tostring(root))
        
        xmlToModels(parse)
        node = exportXML()
        
        assert(node.tag == root.tag)
        nodeList = []
        rootList = []
        root_iter = root.iter()
        for node_child in node.iter():
            nodeList += (node_child,)
        for root_child in root.iter():
            rootList += (root_child,)
"""
