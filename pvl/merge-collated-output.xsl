<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs" version="2.0">
    <xsl:output method="xhtml" indent="no"/>
    <xsl:strip-space elements="*"/>
    <xsl:variable name="manuscripts">
        <sigMapping pointer="#lav" siglum="Lav"/>
        <sigMapping pointer="#tro" siglum="Tro"/>
        <sigMapping pointer="#aka" siglum="Aka"/>
        <sigMapping pointer="#rad" siglum="Rad"/>
        <sigMapping pointer="#ipa" siglum="Ipa"/>
        <sigMapping pointer="#xle" siglum="Xle"/>
        <sigMapping pointer="#kom" siglum="Kom"/>
        <sigMapping pointer="#nak" siglum="NAk"/>
        <sigMapping pointer="#tol" siglum="Tol"/>
    </xsl:variable>
    <xsl:variable name="editions">
        <sigMapping pointer="#bych" siglum="Byč"/>
        <sigMapping pointer="#shakh" siglum="Šax"/>
        <sigMapping pointer="#likh" siglum="Lix"/>
    </xsl:variable>
    <xsl:variable name="paradosis">
        <sigMapping pointer="#lem" siglum="α"/>
    </xsl:variable>
    <xsl:variable name="karskij_blocks" as="document-node()+"
        select="collection('blocks/collatexOutput/?select=*.xml')"/>
    <xsl:template name="main">
        <html>
            <head>
                <title>e-PVL</title>
                <link rel="stylesheet" type="text/css" href="http://www.obdurodon.org/css/style.css"/>
                <link rel="stylesheet" type="text/css" href="css/pvl.css"/>
                <link rel="stylesheet" type="text/css" href="css/collate.css"/>
            </head>
            <body>
                <xsl:apply-templates select="$karskij_blocks/witnesses"/>
            </body>
        </html>
    </xsl:template>
    <xsl:template match="witnesses">
        <xsl:variable name="currentBlockSet" select="." as="element(witnesses)"/>
        <xsl:text>&#x0a;</xsl:text>
        <h2>
            <xsl:value-of select="(.//@u[string-length() gt 0])[1]"/>
        </h2>
        <xsl:text>&#x0a;</xsl:text>
        <div>
            <xsl:text>&#x0a;</xsl:text>
            <table>
                <xsl:text>&#x0a;</xsl:text>
                <tbody class="manuscripts">
                    <xsl:text>&#x0a;</xsl:text>
                    <xsl:for-each select="$manuscripts/sigMapping/@pointer">
                        <xsl:apply-templates
                            select="$currentBlockSet/block[1]/token/@witness[. = current()]">
                            <xsl:with-param name="currentBlockSet" select="$currentBlockSet"/>
                        </xsl:apply-templates>
                    </xsl:for-each>
                </tbody>
                <xsl:text>&#x0a;</xsl:text>
                <tbody class="editions">
                    <xsl:text>&#x0a;</xsl:text>
                    <xsl:for-each select="$editions/sigMapping/@pointer">
                        <xsl:apply-templates
                            select="$currentBlockSet/block[1]/token/@witness[. = current()]">
                            <xsl:with-param name="currentBlockSet" select="$currentBlockSet"/>
                        </xsl:apply-templates>
                    </xsl:for-each>
                </tbody>
                <xsl:text>&#x0a;</xsl:text>
                <tbody class="lemma">
                    <xsl:text>&#x0a;</xsl:text>
                    <xsl:for-each select="$paradosis/sigMapping/@pointer">
                        <xsl:apply-templates
                            select="$currentBlockSet/block[1]/token/@witness[. = current()]">
                            <xsl:with-param name="currentBlockSet" select="$currentBlockSet"/>
                        </xsl:apply-templates>
                    </xsl:for-each>
                </tbody>
                <xsl:text>&#x0a;</xsl:text>
            </table>
            <xsl:text>&#x0a;</xsl:text>
            <xsl:apply-templates/>
        </div>
        <xsl:text>&#x0a;</xsl:text>
    </xsl:template>
    <xsl:template match="block">
        <xsl:variable name="currentBlock" select="." as="element(block)"/>
        <table>
            <xsl:text>&#x0a;</xsl:text>
            <tbody class="manuscripts">
                <xsl:text>&#x0a;</xsl:text>
                <xsl:for-each select="$manuscripts/sigMapping/@pointer">
                    <xsl:apply-templates select="$currentBlock/token[@witness = current()]"/>
                </xsl:for-each>
            </tbody>
            <xsl:text>&#x0a;</xsl:text>
            <tbody class="editions">
                <xsl:text>&#x0a;</xsl:text>
                <xsl:for-each select="$editions/sigMapping/@pointer">
                    <xsl:apply-templates select="$currentBlock/token[@witness = current()]"/>
                </xsl:for-each>
            </tbody>
            <xsl:text>&#x0a;</xsl:text>
            <tbody class="lemma">
                <xsl:text>&#x0a;</xsl:text>
                <xsl:for-each select="$paradosis/sigMapping/@pointer">
                    <xsl:apply-templates select="$currentBlock/token[@witness = current()]"/>
                </xsl:for-each>
            </tbody>
            <xsl:text>&#x0a;</xsl:text>
        </table>
        <xsl:text>&#x0a;</xsl:text>
    </xsl:template>
    <xsl:template match="token">
        <tr>
            <td>
                <xsl:choose>
                    <xsl:when test="boolean(./node())">
                        <xsl:apply-templates/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:text>&#xa0;</xsl:text>
                    </xsl:otherwise>
                </xsl:choose>
            </td>
        </tr>
        <xsl:text>&#x0a;</xsl:text>
    </xsl:template>
    <xsl:template match="hi[@rend='sup']">
        <sup>
            <xsl:apply-templates/>
        </sup>
    </xsl:template>
    <xsl:template match="@witness">
        <tr>
            <th>
                <xsl:value-of
                    select="($manuscripts|$editions|$paradosis)/sigMapping[@pointer = current()]/@siglum"
                />
            </th>
        </tr>
        <xsl:text>&#x0a;</xsl:text>
    </xsl:template>
</xsl:stylesheet>
