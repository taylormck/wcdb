#!/usr/bin/env python

import xml.etree.cElementTree as ET
import sys

toParse = "test.xml"

if len(sys.argv) > 1:   
    toParse = sys.argv[1]

#Done to prevent Billion Laughs Attack
parser = ET.XMLParser()

tree = ET.parse(toParse)

ET.dump(tree)

