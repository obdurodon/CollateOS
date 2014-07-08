<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs" version="2.0">
    <xsl:output method="xhtml" indent="no" doctype-system="about:legacy-compat"/>
    <xsl:strip-space elements="*"/>
    <xsl:variable name="witnesses" as="element(witness)+">
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
    <xsl:template match="collationOutput">
        <html>
            <head>
                <title>PVL test output</title>
                <link rel="stylesheet" type="text/css" href="http://www.obdurodon.org/css/style.css"/>
                <link rel="stylesheet" type="text/css" href="http://pvl.obdurodon.org/css/pvl.css"/>
            </head>
            <body>
                <xsl:apply-templates/>
            </body>
        </html>
    </xsl:template>
    <xsl:template match="line">
        <xsl:variable name="line" select="."/>
        <h4>
            <xsl:value-of select="block[1]/token[1]/@u"/>
        </h4>
        <xsl:text>&#x0a;</xsl:text>
        <table>
            <xsl:text>&#x0a;</xsl:text>
            <tbody class="manuscripts">
                <xsl:text>&#x0a;</xsl:text>
                <xsl:for-each
                    select="'#lav','#tro','#rad','#aka','#ipa','#xle','#kom','#nak','#tol'">
                    <xsl:apply-templates select="$line/block[token[1]/@witness eq current()]"/>
                    <xsl:text>&#x0a;</xsl:text>
                </xsl:for-each>
            </tbody>
            <xsl:text>&#x0a;</xsl:text>
            <tbody class="editions">
                <xsl:text>&#x0a;</xsl:text>
                <xsl:for-each select="'#bych','#shakh','#likh'">
                    <xsl:apply-templates select="$line/block[token[1]/@witness eq current()]"/>
                    <xsl:text>&#x0a;</xsl:text>
                </xsl:for-each>
            </tbody>
            <xsl:text>&#x0a;</xsl:text>
            <tbody class="lemma">
                <xsl:text>&#x0a;</xsl:text>
                <xsl:apply-templates select="$line/block[token[1]/@witness eq '#lem']"/>
                <xsl:text>&#x0a;</xsl:text>
            </tbody>
            <xsl:text>&#x0a;</xsl:text>
        </table>
        <xsl:text>&#x0a;</xsl:text>
    </xsl:template>
    <xsl:template match="block">
        <xsl:text>  </xsl:text>
        <tr>
            <xsl:text>&#x0a;    </xsl:text>
            <th>
                <xsl:value-of select="$witnesses[@pointer eq current()/token[1]/@witness]/@siglum"/>
            </th>
            <xsl:text>&#x0a;</xsl:text>
            <xsl:apply-templates/>
            <xsl:text>  </xsl:text>
        </tr>
    </xsl:template>
    <xsl:template match="token">
        <xsl:text>     </xsl:text>
        <td class="os">
            <xsl:choose>
                <xsl:when test="string-length(normalize-space(.)) gt 0">
                    <xsl:attribute name="data-n" select="@n"/>
                    <xsl:apply-templates/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:text>&#xa0;</xsl:text>
                </xsl:otherwise>
            </xsl:choose>
        </td>
        <xsl:text>&#x0a;</xsl:text>
    </xsl:template>
    <xsl:template match="hi">
        <sup>
            <xsl:apply-templates/>
        </sup>
    </xsl:template>
    <xsl:template match="lb">
        <xsl:text> | </xsl:text>
    </xsl:template>
    <xsl:template match="pb">
        <xsl:text> |[</xsl:text>
        <xsl:value-of select="@n"/>
        <xsl:text>]| </xsl:text>
    </xsl:template>
    <xsl:template match="choide">
        <xsl:text> {</xsl:text>
        <xsl:apply-templates/>
        <xsl:text>} </xsl:text>
    </xsl:template>
    <xsl:template match="seg">
        <xsl:if test="preceding-sibling::seg">
            <xsl:text> | </xsl:text>
        </xsl:if>
        <xsl:apply-templates/>
    </xsl:template>
</xsl:stylesheet>
