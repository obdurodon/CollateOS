<?xml version="1.0" encoding="UTF-8"?>
<!-- 
    tei-add-word-tags.xsl
    2014-02-06 djb
    
    adds <w> tags around words in TEI ms transcriptions 
    $first replaces \s+ in p/text() with <wb/>
        to do: this will break if there is something like <add> ... </add> with multiple words
    $second copies the <teiHeader> and then applies templates to the <text>
        the templates take groups starting with <wb/> and wrap <w> tags around
        erroneously tags isolated punctuation, such as ":~", as well as isolated <lb/>
    $third fixes the isolated bits by uniting them with what precedes
        to do: not handling <pb/>
    
    to do: <add> may contain a string of words
-->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="#all"
    xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns="http://www.tei-c.org/ns/1.0"
    xpath-default-namespace="http://www.tei-c.org/ns/1.0" version="2.0">
    <xsl:strip-space elements="*"/>
    <xsl:output method="xml" indent="no"/>
    <xsl:template match="/">
        <xsl:variable name="first">
            <xsl:apply-templates select="node()" mode="first"/>
        </xsl:variable>
        <xsl:variable name="second">
            <xsl:apply-templates select="$first//text" mode="second"/>
        </xsl:variable>
        <TEI>
            <xsl:copy-of select="TEI/teiHeader"/>
            <xsl:apply-templates select="$second" mode="third"/>
        </TEI>
    </xsl:template>
    <xsl:template match="node()|@*" mode="#all">
        <xsl:copy>
            <xsl:apply-templates select="node()|@*" mode="#current"/>
        </xsl:copy>
    </xsl:template>
    <xsl:template match="body/div/p/text()" mode="first">
        <xsl:analyze-string select="." regex="\s+">
            <xsl:matching-substring>
                <wb/>
            </xsl:matching-substring>
            <xsl:non-matching-substring>
                <xsl:sequence select="."/>
            </xsl:non-matching-substring>
        </xsl:analyze-string>
    </xsl:template>
    <xsl:template match="p" mode="second">
        <p>
            <xsl:for-each-group select="node()" group-starting-with="wb">
                <xsl:text>&#x0a;</xsl:text>
                <w>
                    <xsl:apply-templates select="current-group()[not(self::wb)]" mode="second"/>
                </w>
            </xsl:for-each-group>
        </p>
    </xsl:template>
    <xsl:template match="w" mode="third">
        <!-- 
            If a <w> consists entirely of a <lb/> (node()[1][self::lb], omit it,
            but add the <lb/>, with a leading space, to the preceding <w> 
        -->
        <xsl:choose>
            <xsl:when test="following-sibling::w[1]/node()[1][self::lb]">
                <w>
                    <xsl:apply-templates select="node()|@*"/>
                    <xsl:text> </xsl:text>
                    <lb/>
                </w>
            </xsl:when>
            <xsl:when test="matches(following-sibling::w[1]/node()[1],'^\P{L}+$')">
                <w>
                    <xsl:apply-templates select="node()|@*"/>
                    <xsl:text> </xsl:text>
                    <xsl:value-of select="following-sibling::w[1]/node()[1]"/>
                </w>
            </xsl:when>
            <xsl:when
                test="node()[1][self::lb] or matches(.,'^\P{L}+$') or (string-length(normalize-space(.)) eq 0 and not(*))"/>
            <xsl:otherwise>
                <w>
                    <xsl:apply-templates/>
                </w>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
</xsl:stylesheet>
