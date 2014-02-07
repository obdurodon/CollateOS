<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs" version="2.0"
    xmlns="http://www.w3.org/1999/xhtml" xpath-default-namespace="http://www.w3.org/1999/xhtml">
    <xsl:strip-space elements="*"/>
    <xsl:output method="xhtml" indent="yes" doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN"
        doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"/>
    <xsl:variable name="labels" as="element(table)">
        <xsl:copy-of select="//body/table[1]"/>
    </xsl:variable>
    <xsl:template match="*|@*">
        <xsl:copy>
            <xsl:apply-templates select="node()|@*"/>
        </xsl:copy>
    </xsl:template>
    <xsl:template match="body">
        <xsl:copy>
            <xsl:for-each-group select="table[position() gt 1]"
                group-starting-with="table[position() mod 6 = 2]">
                <div>
                    <h3>
                        <xsl:text>Group </xsl:text>
                        <xsl:value-of select="position()"/>
                    </h3>
                    <xsl:sequence select="$labels"/>
                    <xsl:apply-templates select="current-group()"/>
                </div>
            </xsl:for-each-group>
        </xsl:copy>
    </xsl:template>
    <xsl:template match="text()">
        <xsl:value-of select="normalize-space(.)"/>
    </xsl:template>
    <xsl:template match="hi[@rend='sup']">
        <sup>
            <xsl:apply-templates/>
        </sup>
    </xsl:template>
    <xsl:template match="lb">
        <xsl:text>|</xsl:text>
    </xsl:template>
</xsl:stylesheet>
