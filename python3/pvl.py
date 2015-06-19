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
        print(json.dumps(self.root,ensure_ascii=False,indent=2))
        
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
                <xsl:with-param name="input" select="normalize-space(.)"/>
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
                <xsl:copy-of select="following::node()[count(. | $tooFar) != count($tooFar)]"/>
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
        self.witContentsWWrappers = Witness.transformWrapW(self.witContentsWMilestones)
        self.witWords = self.witContentsWWrappers.xpath('w')
        self.witData = {}
        self.tokenList = []
        for word in self.witWords:
            stringified = etree.tostring(word, encoding='unicode')
            stripped = Witness.witRegex.match(stringified).group(1)
            token = {}
            token['t'] = stripped
            token['n'] = stripped
            self.tokenList.append(token)
        self.witData['id'] = self.witIdentifier
        self.witData['tokens'] = self.tokenList

class Word:
    'An instance of Word represents a word from a witness, which serves as a collation token'
    def soundex(self):
        return 'hi:' + self + ':bye'

def main():
    tree = etree.parse('01_input_xml/pvl-1.xml')
    blocks = tree.xpath('//block')
    for item in blocks:
        block = Block(item) 
    print('Done!')

if __name__ == "__main__": main()