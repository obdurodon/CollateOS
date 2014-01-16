# -*- coding: utf-8 -*-
import codecs, os, sys, xml.dom.minidom as minidom
path = r'../sample_ms_files/scholia'
getRidOf = ['lacuna', 'sup', 'sub']

def stripPunct(string):
    """Remove punctuation from a given string"""
    punct = u'̈҃ⸯ·҇!#$%&=\'()*+,-.:;?@[\\]^_`{|}~'
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

def stripElements(elements, string):
    """Remove given xml element tags from the string, keeping their text contents"""
    for element in elements:
        for exclude in ['<' + element + '>', '</' + element + '>', '<' + element + '/>']:
            string = string.replace(exclude, '')
    return string

def splitTagsFromText(string):
    """Helper function to split text to xml tags and text. Useful when you din't want operation to alter contents of the tag"""
    opens = '<'
    closes = '>'
    stack = []
    result = []
    for char in string:
        pos = opens.find(char)
        if pos >= 0:
            if result and not stack:
               yield ''.join(result)
               result = []
            result.append(char)
            stack.append(closes[pos])
            continue
        result.append(char)
        pos = closes.find(char)
        if pos >= 0:
            stack.pop()
            if not stack: 
                yield ''.join(result)
                result = []
    if result:
        yield ''.join(result)

def conflate(string):
    """Execute conflation rules in a given order"""
    rules = minidom.parse(r'soundex-rules.xml')
    vowels = minidom.parse(r'vowels.xml')
    vowelList = [v.firstChild.nodeValue for v in vowels.getElementsByTagName('vowel')]
    manyToOne = rules.getElementsByTagName('manyToOne')[0].getElementsByTagName('set')   
    oneToMany = rules.getElementsByTagName('oneToMany')[0].getElementsByTagName('set')
    oneToOne = rules.getElementsByTagName('oneToOne')[0].getElementsByTagName('set')
    generalVowels = vowels.getElementsByTagName('general')[0].getElementsByTagName('vowel')
    specialVowels = vowels.getElementsByTagName('special')[0].getElementsByTagName('vowel')
    for rule in manyToOne:
        string = string.replace(rule.getElementsByTagName('in')[0].firstChild.nodeValue, rule.getElementsByTagName('out')[0].firstChild.nodeValue)
    for rule in oneToMany:
        string = string.replace(rule.getElementsByTagName('in')[0].firstChild.nodeValue, rule.getElementsByTagName('out')[0].firstChild.nodeValue)
    for rule in oneToOne:
        string = string.replace(rule.getElementsByTagName('in')[0].firstChild.nodeValue, rule.getElementsByTagName('out')[0].firstChild.nodeValue)
    for vowel in specialVowels:
        string = string.replace(vowel.firstChild.nodeValue, '') # entirely eliminating vowels in the special category from all words
    temp = []
    for i in list(splitTagsFromText(xmlDoc)):
        if i.startswith('<'):
            temp.append(i)
        else:
            words = i.split()
            newWords = []
            for word in words:
                newWord = [word[0]] # Keep the first character even if it's a vowel
                degeminated = reduce(lambda x, y: x+y if x[-1:]!=y else x, word, "") # remove one of the letters if found a geminate pair
                for char in degeminated[1:]: #Appendonly consonants starting at the char in position 1
                    if not char in vowelList:
                        newWord.append(char)
##                print word, ''.join(newWord) ##Uncomment to see word by word change after all the rules up to this point have taken effect
                newWords.append(''.join(newWord))
            temp.extend(newWords)
    string = ' '.join(temp)
    return string
for f in filter(lambda x: str(x.split('.')[len(x.split('.'))-1]) == 'xml' , os.listdir(path)):
    xmlDoc = stripElements(getRidOf, stripPunct(codecs.open(os.path.join(path, f), 'r', encoding='UTF-8').read()))
    print conflate(xmlDoc)
