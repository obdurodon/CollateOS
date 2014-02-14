<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="#all" version="2.0"
    xmlns="http://www.tei-c.org/ns/1.0">
    <xsl:strip-space elements="*"/>
    <xsl:output method="xml" indent="yes"/>
    <xsl:template match="/">
        <xsl:comment>xml-model href="http://www.tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"</xsl:comment>
        <xsl:comment>xml-model href="http://www.tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng" type="application/xml" schematypens="http://purl.oclc.org/dsdl/schematron"</xsl:comment>
        <xsl:apply-templates/>
    </xsl:template>
    <xsl:template match="pvl">
        <TEI>
            <teiHeader>
                <fileDesc>
                    <titleStmt>
                        <title>Rusʹ primary chronicle</title>
                    </titleStmt>
                    <publicationStmt>
                        <p>TEI version prepared by David J. Birnbaum (djbpitt@gmail.com,
                            http://www.obdurodon.org) for the Harvard University Research
                            Institute.</p>
                    </publicationStmt>
                    <sourceDesc>
                        <list>
                            <item>Paper publication by Harvard University Press, 2003 [2004], edited
                                by Donald Ostrowski, with David J. Birnbaum (associate editor) and
                                Horace G. Lunt (senior consultant). ISBN 9780916458911.</item>
                            <item>The digital edition and paper publication were derived from the
                                same troff source files. That is, except for corrections (see
                                below), they have the same content, but neither is textually
                                secondary to the other.</item>
                            <item>Digital edition includes corrections to the paper edition as
                                published at
                                http://hudce7.harvard.edu/~ostrowski/pvl/pvlchanges.pdf.</item>
                        </list>
                        <listWit>
                            <witness xml:id="lav">
                                <choice>
                                    <abbr>Lav</abbr>
                                    <expan>Laurentian</expan>
                                </choice>
                            </witness>
                            <witness xml:id="tro">
                                <choice>
                                    <abbr>Tro</abbr>
                                    <expan>Trinity</expan>
                                </choice>
                            </witness>
                            <witness xml:id="rad">
                                <choice>
                                    <abbr>Rad</abbr>
                                    <expan>Radziwiłł</expan>
                                </choice>
                            </witness>
                            <witness xml:id="aka">
                                <choice>
                                    <abbr>Aka</abbr>
                                    <expan>Academy</expan>
                                </choice>
                            </witness>
                            <witness xml:id="ipa">
                                <choice>
                                    <abbr>Ipa</abbr>
                                    <expan>Hypatian</expan>
                                </choice>
                            </witness>
                            <witness xml:id="xle">
                                <choice>
                                    <abbr>Xle</abbr>
                                    <expan>Xlebnikov</expan>
                                </choice>
                            </witness>
                            <witness xml:id="kom">
                                <choice>
                                    <abbr>Kom</abbr>
                                    <expan>Commission (Novg I)</expan>
                                </choice>
                            </witness>
                            <witness xml:id="tol">
                                <choice>
                                    <abbr>Tol</abbr>
                                    <expan>Tolstoy (Novg I)</expan>
                                </choice>
                            </witness>
                            <witness xml:id="nak">
                                <choice>
                                    <abbr>NAk</abbr>
                                    <expan>Academy (Novg I)</expan>
                                </choice>
                            </witness>
                            <witness xml:id="bych">
                                <choice>
                                    <abbr>Byč</abbr>
                                    <expan>Byčkov</expan>
                                </choice>
                            </witness>
                            <witness xml:id="shakh">
                                <choice>
                                    <abbr>Šax</abbr>
                                    <expan>Šaxmatov</expan>
                                </choice>
                            </witness>
                            <witness xml:id="likh">
                                <choice>
                                    <abbr>Lix</abbr>
                                    <expan>Lixačev</expan>
                                </choice>
                            </witness>
                        </listWit>
                    </sourceDesc>
                </fileDesc>
                <encodingDesc>
                    <p>In the print edition, <emph>angle brackets</emph> are used to indicate
                        problematic material of any kind (illegibility, physical damage, correction,
                        text that has been crossed out). In the TEI edition those areas are tagged
                        as <gi>sic</gi>.</p>
                    <p>In the print edition <emph>square brackets</emph> are used to indicate
                        marginal additions. In the TEI edition those areas are tagged as <tag>add
                            place="margin"</tag>.</p>
                    <p>Text that is missing for any reason (e.g., damage in the original, never part
                        of the original) is tagged as <gi>gap</gi>.</p>
                </encodingDesc>
            </teiHeader>
            <text>
                <body>
                    <xsl:apply-templates/>
                </body>
            </text>
        </TEI>
    </xsl:template>
    <xsl:template match="block">
        <xsl:if test="position() = 1 or @column ne preceding-sibling::block[1]/@column">
            <milestone unit="column" n="{@column}"/>
        </xsl:if>
        <div type="block" n="{@line}">
            <p>
                <app>
                    <lem>
                        <xsl:apply-templates select="paradosis"/>
                    </lem>
                    <rdgGrp type="manuscripts">
                        <xsl:apply-templates select="manuscripts"/>
                    </rdgGrp>
                    <rdgGrp type="editions">
                        <xsl:apply-templates select="* except (manuscripts | paradosis)"/>
                    </rdgGrp>
                </app>
            </p>
        </div>
    </xsl:template>
    <xsl:template match="manuscripts/* | block/*[not(self::manuscripts | self::paradosis)]">
        <rdg wit="#{lower-case(local-name(.))}">
            <xsl:apply-templates/>
        </rdg>
    </xsl:template>
    <xsl:template match="sup">
        <hi rend="sup">
            <xsl:apply-templates/>
        </hi>
    </xsl:template>
    <xsl:template match="sub">
        <hi rend="sub">
            <xsl:apply-templates/>
        </hi>
    </xsl:template>
    <xsl:template match="pageRef">
        <pb n="{.}"/>
    </xsl:template>
    <xsl:template match="lb">
        <lb/>
    </xsl:template>
    <xsl:template match="problem">
        <sic>
            <xsl:apply-templates/>
        </sic>
    </xsl:template>
    <xsl:template match="marginalia">
        <add place="margin">
            <xsl:apply-templates/>
        </add>
    </xsl:template>
    <xsl:template match="omitted">
        <gap/>
    </xsl:template>
    <xsl:template match="choice">
        <choice>
            <xsl:apply-templates/>
        </choice>
    </xsl:template>
    <xsl:template match="option">
        <seg>
            <xsl:apply-templates/>
        </seg>
    </xsl:template>
</xsl:stylesheet>
