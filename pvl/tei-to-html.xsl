<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="#all"
    xpath-default-namespace="http://www.tei-c.org/ns/1.0" xmlns="http://www.w3.org/1999/xhtml"
    version="2.0">
    <xsl:strip-space elements="*"/>
    <xsl:output method="xhtml" indent="yes"/>
    <xsl:key name="witnessBySiglum" match="witness" use="@xml:id"/>
    <xsl:template match="TEI">
        <html>
            <head>
                <link rel="stylesheet" type="text/css" href="http://www.obdurodon.org/css/style.css"/>
                <link rel="stylesheet" type="text/css" href="css/pvl.css"/>
                <title>
                    <xsl:apply-templates select="teiHeader/fileDesc/titleStmt/title"/>
                </title>
            </head>
            <body>
                <xsl:apply-templates select="text/body/div"/>
            </body>
        </html>
    </xsl:template>
    <xsl:template match="div">
        <h3>
            <xsl:value-of select="preceding-sibling::milestone[1]/@n"/>
            <xsl:text>, </xsl:text>
            <xsl:value-of select="@n"/>
        </h3>
        <table>
            <xsl:apply-templates/>
        </table>
    </xsl:template>
    <xsl:template match="app">
        <xsl:apply-templates select="rdgGrp, lem"/>
    </xsl:template>
    <xsl:template match="rdgGrp">
        <tbody class="{@type}">
            <xsl:apply-templates/>
        </tbody>
    </xsl:template>
    <xsl:template match="rdg">
        <tr>
            <th>
                <xsl:value-of select="key('witnessBySiglum',substring(@wit,2))/choice/abbr"/>
            </th>
            <td>
                <xsl:apply-templates/>
            </td>
        </tr>
    </xsl:template>
    <xsl:template match="lem">
        <tbody class="lemma">
            <tr>
                <th>α</th>
                <td>
                    <xsl:apply-templates/>
                </td>
            </tr>
        </tbody>
    </xsl:template>
    <xsl:template match="lb">
        <xsl:text>|</xsl:text>
    </xsl:template>
    <xsl:template match="pb">
        <xsl:text>[</xsl:text>
        <xsl:value-of select="@n"/>
        <xsl:text>]</xsl:text>
    </xsl:template>
    <xsl:template match="hi">
        <xsl:choose>
            <xsl:when test="@rend = 'sup'">
                <sup>
                    <xsl:apply-templates/>
                </sup>
            </xsl:when>
            <xsl:when test="@rend = 'sub'">
                <sub>
                    <xsl:apply-templates/>
                </sub>
            </xsl:when>
            <xsl:otherwise>
                <xsl:message>Error</xsl:message>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template match="sic">
        <xsl:text>&lt;</xsl:text>
        <xsl:apply-templates/>
        <xsl:text>&gt;</xsl:text>
    </xsl:template>
    <xsl:template match="add">
        <xsl:text>[</xsl:text>
        <xsl:apply-templates/>
        <xsl:text>]</xsl:text>
    </xsl:template>
    <xsl:template match="gap">
        <xsl:text>[lacuna]</xsl:text>
    </xsl:template>
    <xsl:template match="choice">
        <xsl:text>{</xsl:text>
        <xsl:apply-templates/>
        <xsl:text>}</xsl:text>
    </xsl:template>
    <xsl:template match="seg[preceding-sibling::sig]">
        <xsl:text>/</xsl:text>
        <xsl:apply-templates/>
    </xsl:template>
</xsl:stylesheet>
