<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs" version="2.0"
    xmlns="http://www.w3.org/1999/xhtml">
    <xsl:output method="xhtml" indent="yes"/>
    <xsl:variable name="sigla" select="distinct-values(//@witness)" as="xs:string+"/>
    <xsl:variable name="karskij" select="/witnesses/block[1]/token[1]/@u" as="xs:string"/>
    <xsl:variable name="witnesses" as="element()+">
        <witness pointer="#lav" siglum="Lav"/>
        <witness pointer="#tro" siglum="Tro"/>
        <witness pointer="#rad" siglum="Rad"/>
        <witness pointer="#aka" siglum="Aka"/>
        <witness pointer="#ipa" siglum="Ipa"/>
        <witness pointer="#xle" siglum="Xle"/>
        <witness pointer="#kom" siglum="Kom"/>
        <witness pointer="#nak" siglum="NAk"/>
        <witness pointer="#tol" siglum="Tol"/>
        <witness pointer="#bych" siglum="Byč"/>
        <witness pointer="#shakh" siglum="Šax"/>
        <witness pointer="#likh" siglum="Lix"/>
        <witness pointer="#lem" siglum="α"/>
    </xsl:variable>
    <xsl:template match="witnesses">
        <html>
            <head>
                <title>
                    <xsl:value-of select="$karskij"/>
                </title>
                <link rel="stylesheet" type="text/css" href="css/pvl.css"/>
                <link rel="stylesheet" type="text/css" href="http://www.obdurodon.org/css/style.css"/>
                <link rel="stylesheet" type="text/css" href="css/collate.css"/>

            </head>
            <body>
                <h1>
                    <xsl:value-of select="$karskij"/>
                </h1>
                <div>
                    <table>
                        <tbody class="manuscripts">
                            <xsl:for-each select="$witnesses[position() lt 10]">
                                <xsl:if test="current()/@pointer = $sigla">
                                    <tr>
                                        <th>
                                            <xsl:value-of select="current()/@siglum"/>
                                        </th>
                                    </tr>
                                </xsl:if>
                            </xsl:for-each>
                        </tbody>
                        <tbody class="editions">
                            <xsl:for-each select="$witnesses[position() gt 9][position() lt 13]">
                                <xsl:if test="current()/@pointer = $sigla">
                                    <tr>
                                        <th>
                                            <xsl:value-of select="current()/@siglum"/>
                                        </th>
                                    </tr>
                                </xsl:if>
                            </xsl:for-each>
                        </tbody>
                        <tbody class="lemma">
                            <xsl:if test="$witnesses[13] = $sigla">
                                <tr>
                                    <th>
                                        <xsl:value-of select="current()/@siglum"/>
                                    </th>
                                </tr>
                            </xsl:if>
                        </tbody>
                    </table>
                    <xsl:apply-templates/>
                </div>
            </body>
        </html>
    </xsl:template>
    <xsl:template match="block">
        <table>
            <tbody class="manuscripts">
                <xsl:apply-templates select="token[@witness = '#lav']"/>
                <xsl:apply-templates select="token[@witness = '#tro']"/>
                <xsl:apply-templates select="token[@witness = '#rad']"/>
                <xsl:apply-templates select="token[@witness = '#aka']"/>
                <xsl:apply-templates select="token[@witness = '#ipa']"/>
                <xsl:apply-templates select="token[@witness = '#xle']"/>
                <xsl:apply-templates select="token[@witness = '#kom']"/>
                <xsl:apply-templates select="token[@witness = '#nak']"/>
                <xsl:apply-templates select="token[@witness = '#tol']"/>
            </tbody>
            <tbody class="editions">
                <xsl:apply-templates select="token[@witness = '#bych']"/>
                <xsl:apply-templates select="token[@witness = '#shakh']"/>
                <xsl:apply-templates select="token[@witness = '#likh']"/>
            </tbody>
            <tbody class="lemma">
                <xsl:apply-templates select="token[@witness = '#lem']"/>
            </tbody>
        </table>
    </xsl:template>
    <xsl:template match="token">
        <tr>
            <td>
                <xsl:apply-templates/>
            </td>
        </tr>
    </xsl:template>
    <xsl:template match="hi[@rend='sup']">
        <sup>
            <xsl:apply-templates/>
        </sup>
    </xsl:template>
</xsl:stylesheet>
