<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs" version="2.0"
    xpath-default-namespace="http://www.tei-c.org/ns/1.0"
    xmlns:cx="http://interedition.eu/collatex/ns/1.0" xmlns="http://www.w3.org/1999/xhtml">
    <xsl:output method="xhtml" indent="yes"/>
    <xsl:strip-space elements="*"/>
    <xsl:template match="/">
        <html>
            <head>
                <title>test</title>
                <meta http-equiv="content-type" content="application/xhtml+xml; charset=UTF-8"/>
            </head>
            <body>
                <table border="1">
                    <xsl:apply-templates/>
                </table>
            </body>
        </html>
    </xsl:template>
    <xsl:template match="cx:apparatus/text()">
        <tr>
            <td>
                <xsl:text>Text # </xsl:text>
                <xsl:value-of select="position()"/>
            </td>
            <td>
                <xsl:value-of select="."/>
                <xsl:text> </xsl:text>
            </td>
        </tr>
    </xsl:template>
    <xsl:template match="app">
        <tr>
            <td>
                <xsl:text>App # </xsl:text>
                <xsl:value-of select="position()"/>
            </td>
            <xsl:apply-templates/>
        </tr>
    </xsl:template>
    <xsl:template match="rdg">
        <td>
            <xsl:apply-templates/>
        </td>
    </xsl:template>
</xsl:stylesheet>
