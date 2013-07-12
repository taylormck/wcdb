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
import crises.models as cm
from scripts.importScript import *

NIFCrisis = """
    <Crisis ID=\"CRI_NRINFL\" Name=\"2013 Northern India Floods\">
        <Kind>Natural Disaster</Kind>
        <Date>2013-06-14</Date>
        <Time>00:00:00</Time>
        <Common>
            <Citations>
                <li>The Hindustan Times</li>
                <li>The Times of India</li>
            </Citations>
            <ExternalLinks>
                <li href=\"http://en.wikipedia.org/wiki/2013_North_India_floods\">Wikipedia</li>
            </ExternalLinks>
            <Images>
                <li embed=\"http://images.jagran.com/ukhand-ss-02-07-13.jpg\" text=\"This is the alt element of the image.\"/>
                <li embed=\"http://timesofindia.indiatimes.com/photo/15357310.cms\"/>\
            </Images>
            <Videos>
                <li embed=\"//www.youtube.com/embed/qV3s7Sa6B6w\"/>
            </Videos>
            <Maps>
                <li embed=\"[fake]\"/>
            </Maps>
            <Feeds>
                <li embed=\"[WHATEVER A FEED URL LOOKS LIKE]\"/>
            </Feeds>
            <Summary>Lorem ipsum...</Summary>
        </Common>
    </Crisis>
"""

class TestImportScript(TestCase):
    # TODO must make sure to make proper XML strings for these
    def test_parsevalidate_01(TestCase):
        testXML = StringIO.StringIO(NIFCrisis)
        assert validateXML(testXML)
        
    def test_parsevalidate_02(TestCase):
        testXML = StringIO.StringIO("<Dragon></NotDragon>")
        assert not validateXML(testXML)
        
    def test_parsevalidate_03(TestCase):
        testXML = StringIO.StringIO("<Dragon><Cooly></Cooly></Dragon>")
        assert not validateXML(testXML)
        
    def test_parseXML_01(self):
        testXML = StringIO.StringIO("<Dragon></Dragon>")
        root = parseXML(testXML)
        assert(root.tag == "Dragon")

    def test_parseXML_02(TestCase):
        testXML = StringIO.StringIO("<Dragon><Cooly></Cooly></Dragon>")
        root = parseXML(testXML)
        child = root.find("Cooly")
        assert(root.tag == "Dragon")
        assert(child is not None)
        assert(child.tag == "Cooly")

    def test_parseXML_03(TestCase):
        testXML = StringIO.StringIO("<Dragon id=\"5\"></Dragon>")
        root = parseXML(testXML)
        assert(root.tag == "Dragon")
        assert(root.get("id") == "5")

    def test_parseCrisis_01(TestCase):
        testElement = et.fromstring(NIFCrisis)
        testDict = {}
        testCrisis = parseCrisis(testElement, testDict)
        testCrisisCopy = cm.Crisis.objects.get(id="CRI_NRINFL")
        assert(testCrisis is not testCrisisCopy)
        assert(testCrisis == testCrisisCopy)

    def test_parseCrisis_02(TestCase):
        pass
        
    def test_parseCrisis_03(TestCase):
        pass
        
    def test_parseOrganization_01(TestCase):
        pass
        
    def test_parseOrganization_02(TestCase):
        pass
        
    def test_parseOrganization_03(TestCase):
        pass
        
    def test_parsePerson_01(TestCase):
        pass
        
    def test_parsePerson_02(TestCase):
        pass
        
    def test_parsePerson_03(TestCase):
        pass
        
    def test_parseCommon_01(TestCase):
        pass
        
    def test_parseCommon_02(TestCase):
        pass
        
    def test_parseCommon_03(TestCase):
        pass
        
    def test_parseListType_01(TestCase):
        pass
        
    def test_parseListType_02(TestCase):
        pass
        
    def test_parseListType_03(TestCase):
        pass
        
    def test_xmlToModels_01(TestCase):
        pass

    def test_xmlToModels_02(TestCase):
        pass

    def test_xmlToModels_03(TestCase):
        pass

class TestExportScript(TestCase):
    pass
