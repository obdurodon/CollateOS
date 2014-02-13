<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="#all" version="2.0"
    xmlns:xhtml="http://www.w3.org/1999/xhtml" xmlns="http://www.w3.org/1999/xhtml">
    <xsl:strip-space elements="*"/>
    <xsl:output method="xhtml" indent="yes" doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN"
        doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"/>
    <xsl:variable name="title" select="//block[1]/token[1]/substring(@witness,1,8)"/>
    <xsl:variable name="labels" as="element(xhtml:table)">
        <table>
            <xsl:for-each select="//block[1]/token/substring-before(@witness,'.')">
                <tr>
                    <td>
                        <xsl:value-of select="current()"/>
                    </td>
                </tr>
            </xsl:for-each>
        </table>
    </xsl:variable>
    <xsl:template match="witnesses">
        <html>
            <head>
                <title>
                    <xsl:value-of select="$title"/>
                </title>
                <link href="http://www.obdurodon.org/css/style.css" rel="stylesheet" type="text/css"/>
                <link href="css/scholia.css" rel="stylesheet" type="text/css"/>
                <link href="css/collate.css" rel="stylesheet" type="text/css"/>
            </head>
            <body>
                <h1>
                    <xsl:sequence select="$title"/>
                </h1>
                <xsl:for-each-group select="block" group-starting-with="block[position() mod 6 = 1]">
                    <div>
                        <h3>
                            <xsl:text>Group </xsl:text>
                            <xsl:value-of select="position()"/>
                        </h3>
                        <xsl:sequence select="$labels"/>
                        <xsl:apply-templates select="current-group()"/>
                    </div>
                </xsl:for-each-group>
            </body>
        </html>
    </xsl:template>
    <xsl:template match="block">
        <table>
            <xsl:apply-templates/>
        </table>
    </xsl:template>
    <xsl:template match="token">
        <tr>
            <td>
                <xsl:choose>
                    <xsl:when test="string-length(.) gt 0">
                        <xsl:apply-templates/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:text>&#xa0;</xsl:text>
                    </xsl:otherwise>
                </xsl:choose>
            </td>
        </tr>
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
