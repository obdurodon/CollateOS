# -*- coding: utf-8 -*-
#Minas Abovyan
#This script is called by others, not ran by itself. Mainly calling collate function, which uses the rest.


import xml.dom.minidom as minidom

def removeElementTags(element, parent): #turn "text <el>text1</el> text2" into "text text1 text2"
    for child in parent.getElementsByTagName(element):
        parent.replaceChild(child.firstChild, child)
def deleteElements(element, parent): #turn "text <el>text1</el> text2" into "text text2"
    for child in parent.getElementsByTagName(element):
        parent.removeChild(child)
def choose(choice):
    found = False
    choices = {'sic': 'corr', 'orig': 'reg', 'abbr': 'expan'} # given the choose tag, take the second one of the options (value in this dictionary)
    for ch in choices:
        if ch in [child.localName for child in choice.childNodes]:
            found = True
            choice.replaceChild(choice.getElementsByTagName(choices[ch])[0].firstChild, choice.getElementsByTagName(ch)[0])
            deleteElements(choices[ch], choice)
            break
    if not found:
        raise Exception("I don't know what to do with this choice element: " + choice.toxml())

def splitTagsFromText(string): #split "text <el> text1 </el> text2 text3" into a list ['text', '<el>', 'text1', '</el>', 'text2 text3']. Is a generator, so should be called as list(splitTagsFromText(string))
    """Create a generaor that splits given string into xml tags and text"""
    result = []
    stack = []
    for char in string:
        if char == '<':
            if result and not stack:
                yield ''.join(result)
                result = []
            result.append(char)
            stack.append('>')
            continue
        result.append(char)
        if char == '>':
            stack.pop()
            if not stack:
                yield ''.join(result)
                result = []
    if result:
        yield ''.join(result)

def stripPunct(string): #rebuild the string stripping punctuation
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

def applyRule(word, ruleSet): #apply rules found in the rule file. match in to out and replace
    """Helper function to conflate. Applies rules from the conflation file"""
    if ruleSet[0].parentNode.localName == 'oneToOne':
        for rule in ruleSet:
            for char in rule.getElementsByTagName('in')[0].firstChild.nodeValue:
                word = word.replace(char, rule.getElementsByTagName('out')[0].firstChild.nodeValue)
        return word
    else:
        for rule in ruleSet:
            return word.replace(rule.getElementsByTagName('in')[0].firstChild.nodeValue, rule.getElementsByTagName('out')[0].firstChild.nodeValue)

def degeminate(word): #turn consecutively repeating characters in a word into singlets
    """Helper function to conflate. Degeminates words."""
    output = ''
    for index, char in enumerate(word):
        if index > 0:
            if word[index] == word[index-1]:
                continue
            output += char
    return output

def padWithZeros(word): # cut the soundex representation down to 4 chars long, or pad it up to being 4 using 0s if it's less than 4
    """Helper function to conflate. Pads words with zeroes or cuts them off to have all words be 4 charslong"""
    if len(word) < 4:
        return word + '0'*(4-len(word))
    elif len(word) > 4:
        return word[:4]
    else:
        return word
    
def conflate(w): # main function that calls all of the above. Currently under reconstruction.
    """Execute conflation rules in a given order"""
    kids = [el for el in w.getElementsByTagName('*')]
    for kid in kids:
        elName = kid.localName
        parent = kid.parentNode
        if elName in ['add', 'hi', 'unclear']:
            removeElementTags(elName, parent)
            break
        elif elName in ['del', 'gap', 'lacuna', 'lb', 'pb']:
            deleteElements(elName, parent)
            break
        elif elName =='choice':
            choose(kid)
            break
    removeElementTags('choice', w)
    rules = minidom.parse(r'soundex-rules.xml')
    vowels = minidom.parse(r'vowels.xml')
    vowelList = [v.firstChild.nodeValue for v in vowels.getElementsByTagName('vowel')]
    manyToOne = rules.getElementsByTagName('manyToOne')[0].getElementsByTagName('set')   
    oneToMany = rules.getElementsByTagName('oneToMany')[0].getElementsByTagName('set')
    oneToOne = rules.getElementsByTagName('oneToOne')[0].getElementsByTagName('set')
    generalVowels = vowels.getElementsByTagName('general')[0].getElementsByTagName('vowel')
    specialVowels = vowels.getElementsByTagName('special')[0].getElementsByTagName('vowel')
    wlist = []
    for i in list(splitTagsFromText(w.toxml())):
        if not i.startswith('<'):
            wlist.append(i)
    word = stripPunct(''.join(wlist))

# apply rules as specified in soundex-rules.xml
    
    word = applyRule(word, manyToOne)
    word = applyRule(word, oneToMany)
    word = applyRule(word, oneToOne)
# entirely eliminating vowels in the special category from all words

    for vowel in specialVowels:
        word = word.replace(vowel.firstChild.nodeValue, '') 
    
# degeminate words, get rid of noninitial vowels
    if len(word) > 0:    
        newWord = word[0] # Keep the first character even if it's a vowel
        degeminated = degeminate(word)
        for char in degeminated[1:]: #Append only consonants starting at the char in position 1
            if not char in vowelList:
                newWord += char
        return padWithZeros(newWord)
    else:
        return ''
