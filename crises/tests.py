"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

We will definitely want to add many many more tests, but for now, 3 per
function will have to do.
"""
# --- imports ---
import StringIO
import xml.etree.cElementTree as et
from django.test import TestCase
from scripts.importScript import *

class TestImportScript(TestCase):
    def test_parsevalidate_01(TestCase):
        testXML = StringIO.StringIO("<Dragon></Dragon>")
        assert validateXML(testXML)
        
    def test_parsevalidate_02(TestCase):
        testXML = StringIO.StringIO("<Dragon></NotDragon>")
        assert not validateXML(testXML)
        
    def test_parsevalidate_03(TestCase):
        testXML = StringIO.StringIO("<Dragon><Cooly></Cooly></Dragon>")
        assert validateXML(testXML)
        
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
        pass

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
