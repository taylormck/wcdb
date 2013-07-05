#!/usr/bin/env python

import xml.etree.cElementTree as ET
import sys

toParse = "test.xml"

if len(sys.argv) > 1:   
    toParse = sys.argv[1]

tree = ET.parse(toParse)

ET.dump(tree)

