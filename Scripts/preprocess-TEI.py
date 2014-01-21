﻿import datetime, os, xml.dom.minidom as minidom

startTime = datetime.datetime.now()

path = r'..\sample_ms_files\scholia'
xmls = filter(lambda x: str(x.split('.')[len(x.split('.'))-1]) == 'xml' , os.listdir(path))

def removeElementTags(element, parent):
    for child in parent.getElementsByTagName(element):
        parent.replaceChild(child.firstChild, child)
def deleteElements(element, parent):
    for child in parent.getElementsByTagName(element):
        parent.removeChild(child)
def choose(choice):
    found = False
    choices = {'sic': 'corr', 'orig': 'reg', 'abbr': 'expan'}
    for ch in choices:
        if ch in [child.localName for child in choice.childNodes]:
            found = True
            choice.replaceChild(choice.getElementsByTagName(choices[ch])[0].firstChild, choice.getElementsByTagName(ch)[0])
            deleteElements(choices[ch], choice)
            break
    if not found:
        raise Exception("I don't know what to do with this choice element: " + choice.toxml())

def splitTagsFromText(string):
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

def applyRule(word, ruleSet):
    """Helper function to conflate. Applies rules from the conflation file"""
    if ruleSet[0].parentNode.localName == 'oneToOne':
        for rule in ruleSet:
            for char in rule.getElementsByTagName('in')[0].firstChild.nodeValue:
                word = word.replace(char, rule.getElementsByTagName('out')[0].firstChild.nodeValue)
        return word
    else:
        for rule in ruleSet:
            return word.replace(rule.getElementsByTagName('in')[0].firstChild.nodeValue, rule.getElementsByTagName('out')[0].firstChild.nodeValue)

def degeminate(word):
    """Helper function to conflate. Degeminates words."""
    output = ''
    for index, char in enumerate(word):
        if index > 0:
            if word[index] == word[index-1]:
                continue
            output += char
    return output

def padWithZeros(word):
    """Helper function to conflate. Pads words with zeroes or cuts them off to have all words be 4 charslong"""
    if len(word) < 4:
        return word + '0'*(4-len(word))
    elif len(word) > 4:
        return word[:4]
    else:
        return word
    
def conflate(word):
    """Execute conflation rules in a given order"""
    rules = minidom.parse(r'soundex-rules.xml')
    vowels = minidom.parse(r'vowels.xml')
    vowelList = [v.firstChild.nodeValue for v in vowels.getElementsByTagName('vowel')]
    manyToOne = rules.getElementsByTagName('manyToOne')[0].getElementsByTagName('set')   
    oneToMany = rules.getElementsByTagName('oneToMany')[0].getElementsByTagName('set')
    oneToOne = rules.getElementsByTagName('oneToOne')[0].getElementsByTagName('set')
    generalVowels = vowels.getElementsByTagName('general')[0].getElementsByTagName('vowel')
    specialVowels = vowels.getElementsByTagName('special')[0].getElementsByTagName('vowel')

# apply rules as specified in soundex-rules.xml
    
    word = applyRule(word, manyToOne)
    word = applyRule(word, oneToMany)
    word = applyRule(word, oneToOne)

# entirely eliminating vowels in the special category from all words

    for vowel in specialVowels:
        word = word.replace(vowel.firstChild.nodeValue, '') 
    
# degeminate words, get rid of noninitial vowels
        
    newWord = word[0] # Keep the first character even if it's a vowel
    degeminated = degeminate(word)
    for char in degeminated[1:]: #Append only consonants starting at the char in position 1
        if not char in vowelList:
            newWord += char

    return padWithZeros(newWord)

##class Word(object):
##    def __init__(self, original, conflated):
##        self.o = original
##        self.c = conflated

for afile in xmls:
    body = minidom.parse(os.path.join(path, afile)).getElementsByTagName('body')[0]
    p = body.getElementsByTagName('p')[0]
    for tag in ['add', 'hi', 'unclear']:
        removeElementTags(tag, p)
    for tag in ['del', 'gap', 'lacuna', 'lb']:
        deleteElements(tag, p)
    for choice in p.getElementsByTagName('choice'):
        choose(choice)
    removeElementTags('choice', p)
    temp = []
    for i in list(splitTagsFromText(stripPunct(p.toxml()))):
        if i.startswith('<'):
            temp.append(i)
        else:
            words = []
            for w in i.split():
                c = conflate(w)
                words.append(c)
##                W = Word(w, c)
##                print w, 'becomes', c)             Uncomment to see word by word conflation results
            temp.extend(words)
    print ' '.join(temp),'\n\n'    

print 'Took', datetime.datetime.now()-startTime, 'to execute'
