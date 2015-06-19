"""
Filename: test.py
Author: David J. Birnbaum (djbpitt@gmail.com; http://www.obdurodon.org)
First version: 2015-06-18
Based on Python 2 / XSLT application developed by Minas Abovyan and David J. Birnbaum
    (http://pvl.obdurodon.org/doc/manual.html)
Input: pvl.xml
"""

from collatex import *
from lxml import etree
import re
witRegex = re.compile('<.*?>\s*(.*)\s*</.*?>',re.DOTALL) # witness contents without wrapper tags

tree = etree.parse('01_input_xml/pvl.xml')
blocks = tree.xpath('//block')
for block in blocks:
    witnesses = block.xpath('manuscripts/* | Bych | Shakh | Likh | paradosis/Ost') # retrieve all witnesses in order
    for witness in witnesses:
        witIdentifier = witness.xpath('name()')
        wrappedWitContents = etree.tostring(witness, encoding='unicode')
        try:
            witContents = witRegex.match(wrappedWitContents).group(1)
        except AttributeError:
            witContents = ''
        words = re.split('\s+',witContents)        
        print(witIdentifier + ': ' + str(len(words)))
print('Done!')