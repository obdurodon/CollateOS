#!/usr/bin/env python3
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
from collatex import *
import re, json

class Block:
    'An instance of Block represents a Karskii block in the PVL edition'
    def __init__(self,block):
        self.block = block
        self.witnessInput = self.block.xpath('manuscripts/* | Bych | Shakh | Likh | paradosis/Ost') # retrieve all witnesses in order
        self.root = {}
        self.allWitnesses = []
        for item in self.witnessInput:
            witness = Witness(item)
            self.allWitnesses.append(witness.witData)
        self.root['witnesses'] = self.allWitnesses
        self.json = json.dumps(self.root,ensure_ascii=False,indent=2)
        self.alignment = collate_pretokenized_json(self.root,output='json')
        self.alignmentJson = json.loads(self.alignment)
    def XMLify(self):
        witnesses = etree.Element('witnesses')
        for block in self.alignmentJson['table']:
            etree.SubElement(witnesses,'block')
            return witnesses

class Witness:
    'An instance of Witness represents a witness line within a Karskii block'
    witRegex = re.compile('<.*?>\s*(.*)\s*</.*?>',re.DOTALL) # witness contents without wrapper tags
    xsltAddW = etree.XML('''
    <xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
        <xsl:output method="xml" indent="no" encoding="UTF-8" omit-xml-declaration="yes"/>
        <xsl:template match="*|@*">
            <xsl:copy>
                <xsl:apply-templates select="node() | @*"/>
            </xsl:copy>
        </xsl:template>
        <xsl:template match="/*">
            <xsl:copy>
                <xsl:apply-templates select="@*"/>
                <w/>
                <xsl:apply-templates/>
            </xsl:copy>
        </xsl:template>
        <!-- convert <add> and <sic> to milestones (and leave them that way) -->
        <xsl:template match="add | sic">
            <xsl:element name="{name()}" n="start"/>
            <xsl:apply-templates/>
            <xsl:element name="{name()}" n="end"/>
        </xsl:template>
        <xsl:template match="text()">
            <xsl:call-template name="whiteSpace">
                <xsl:with-param name="input" select="translate(.,'&#x0a;',' ')"/>
            </xsl:call-template>
        </xsl:template>
        <xsl:template name="whiteSpace">
            <xsl:param name="input"/>
            <xsl:choose>
                <xsl:when test="not(contains($input, ' '))">
                    <xsl:value-of select="$input"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="substring-before($input, ' ')"/>
                    <w/>
                    <xsl:call-template name="whiteSpace">
                        <xsl:with-param name="input" select="substring-after($input,' ')"/>
                    </xsl:call-template>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:template>
    </xsl:stylesheet>
    ''')
    transformAddW = etree.XSLT(xsltAddW)
    xsltWrapW = etree.XML('''
    <xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
        <xsl:output method="xml" indent="no" omit-xml-declaration="yes"/>
        <xsl:template match="/*">
            <xsl:copy>
                <xsl:apply-templates select="w"/>
            </xsl:copy>
        </xsl:template>
        <xsl:template match="w">
            <!-- faking the "except" operator -->
            <xsl:variable name="tooFar" select="following-sibling::w[1] | following-sibling::w[1]/following::node()"/>
            <w>
                <xsl:copy-of select="following-sibling::node()[count(. | $tooFar) != count($tooFar)]"/>
            </w>
        </xsl:template>
    </xsl:stylesheet>    
    ''')
    transformWrapW = etree.XSLT(xsltWrapW)
    def __init__(self,witness):
        self.witness = witness
        self.witIdentifier = self.witness.xpath('name()')
        self.witWrappedContents = etree.tostring(self.witness, encoding='unicode')
        try:
            self.witContents = Witness.witRegex.match(self.witWrappedContents).group(1)
        except AttributeError:
            self.witContents = ''
        self.witContentsWMilestones = Witness.transformAddW(self.witness)
        # print(self.witContentsWMilestones)
        self.witContentsWWrappers = Witness.transformWrapW(self.witContentsWMilestones)
        self.witWords = self.witContentsWWrappers.xpath('w')
        self.witData = {}
        self.tokenList = []
        for item in self.witWords:
            word = Word(item)
            token = {}
            token['t'] = word.unwrapped
            token['n'] = word.noTags
            if word.stringified != '<w/>': # leading spaces in the input generate spurious empty words
                self.tokenList.append(token)
        self.witData['id'] = self.witIdentifier
        self.witData['tokens'] = self.tokenList

class Word:
    'An instance of Word represents a word from a witness, which serves as a collation token'
    unwrapRegex = re.compile('<.*?>\s*(.*)\s*</.*?>')
    puncRegex = re.compile('[“̈҃ⸯ·҇!#$%&=\'()*+,-.:;?@[\\]^_`{|}~”̏′]')
    tagRegex = re.compile('<.*?>')
    # Multiple replacements from: http://stackoverflow.com/questions/6116978/python-replace-multiple-strings
    soundexMappings = {
        "[оу]" : "у",
        "[шт]" : "щ",
        "[ѿ]" : "ѡт",
        "[ѯ]" : "кс",
        "[ѱ]" : "пс",
        "[ѧѩꙙꙝꙗя]" : "ѧ",
        "[еєѥ]" : "е",
        "[ыꙑиіїꙇй]" : "и",
        "[оꙩꙫꙭꙮѡꙍѽѻ]" : "о",
        "[уꙋюꙕѵѷӱѹ]" : "у",
        "[ѫѭꙛ]" : "ѫ",
        "[ѣꙓ]" : "ѣ",
        "[ьъ]" : "ь",
        "[зꙁꙃѕꙅ]" : "з"
    }
    def __init__(self,word):
        self.word = word
        self.stringified = etree.tostring(self.word, encoding='unicode')
        try:
            self.unwrapped = Word.unwrapRegex.match(self.stringified).group(1)
        except AttributeError:
            self.unwrapped = ''
        self.noPunc = Word.puncRegex.sub('',self.stringified)
        self.noTags = Word.tagRegex.sub('',self.noPunc)

def main():
    tree = etree.parse('01_input_xml/pvl-1.xml')
    blocks = tree.xpath('//block')
    for item in blocks:
        block = Block(item) 
        # print(block.alignmentJson['table'])
        print(etree.tostring(block.XMLify(),pretty_print=True))

if __name__ == "__main__": main()