# -*- coding: utf-8 -*-
import codecs, os, sys, xml.dom.minidom as minidom
path = r'../sample_ms_files/scholia'

def stripPunct(string):
    punct = u'҃ⸯ·҇!#$%&=\'()*+,-.:;?@[\\]^_`{|}~'
    assemble = []
    inTag= False
    for char in string:
        if char == '<':
            inTag = True
        elif char == '>':
            inTag = False
        if inTag:
            assemble.append(char) #add char to the output unaltered, if it's inside an xml tag
        elif not char in punct:
            assemble.append(char.lower()) #if charis not part of tag and is not a punctuation mark, add char to the output lowercased
    return ''.join(assemble)

for f in filter(lambda x: str(x.split('.')[len(x.split('.'))-1]) == 'xml' , os.listdir(path)):
    xmlDoc = stripPunct(codecs.open(os.path.join(path, f), 'r', encoding='UTF-8').read())
    print xmlDoc
