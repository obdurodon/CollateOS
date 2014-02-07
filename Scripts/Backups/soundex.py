#!/usr/bin/env python
# -*-coding: utf8-*-
# ==============================================================================
# Filename:  soundex.py
# Developer: David J. Birnbaum (djbpitt@gmail.com; http://www.obdurodon.org)
# Date:      Created 2013-06-28; last modified 2013-06-29
# Summary:   Module to convert early Cyrillic to soundex-like representation
#            See full documentation at ***ADD URL***
# Requires:  sys, codecs, lxml
# License:   Original material is CC BY-NC-SA 
#            http://creativecommons.org/licenses/by-nc-sa/3.0/deed.en_US
# ==============================================================================

# Annoying encoding quirk fixed as per https://pythonadventures.wordpress.com/tag/ascii/
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import codecs
# wrong: import xml.etree.ElementTree as ET; this serializes as numerical character references
# use lxml instead to serialize as raw unicode strings; to install:
#   Mac: macports; Centos: yum; Windows ActivePython: pypm for pil, then lxml
from lxml import etree as ET

#http://stackoverflow.com/questions/11285866/unicodeencodeerror-ascii-codec-cant-encode-character
def __str__(self):
    return self.__repr__().encode(stdout.encoding)

# Mappings from Cyrillic to soundex; first char in each u-string is output target
# http://boredzo.org/blog/archives/2008-06-16/what-to-do-if-python-says-%E2%80%9Ccharacter-mapping-must-return-integer-none-or-unicode%E2%80%9D
a_letters = u'аꙗ'
e_letters = u'еєѥ'
i_letters = u'иыїі'
o_letters = u'оѡ'
u_letters = u'уꙋюѵ'
# z
# conflate geminates, ou
# split ksi, psi, sht, ot
# strip markup
# strip punctuation
# strip non-initial vowels
# conflate
# trim or pad to four u-characters
inlist = [a_letters,e_letters,i_letters,o_letters,u_letters]
intab = u''.join(inlist)
outlist = [x[0] * len(x) for x in inlist ] # copy target once for each char in input
outtab = u''.join(outlist)
trantab = dict(zip(map(ord,intab),outtab))

def soundexify(cyrillic):
    return cyrillic.lower().translate(trantab)

# Build array of input documents
def parse(xml):
    units = {}
    root = ET.parse(xml).getroot()
    xml_units = root.findall(".//unit")
    for unit in xml_units:
        n = unit.attrib['n']
        units['n'] = {}
        for witness in unit.findall("./*"):
            units['n'][witness.tag] = witness
            #outfile.write("unit = " + n + "; witness = " + witness.tag + ", and text = " + ET.tostring(witness,encoding=unicode))
            outfile.write(ET.tostring(witness,encoding=unicode))
            
if __name__ == "__main__":
    infile = codecs.open('APOL1-IC.xml', mode="r", encoding='utf-8')
    outfile = codecs.open('out.xml', mode='w', encoding='utf-8')
    parse(infile)
    infile.close
    outfile.close
    print soundexify(u'аꙗеєѥыиїіоѡуꙋюѵАБВДЕЖ')
        
    
    
    