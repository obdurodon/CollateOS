# -*- coding: utf-8 -*-
#Minas Abovyan
#This script is called by others, not ran by itself. Mainly calling collate function, which uses the rest.


import re, sys, xml.dom.minidom as minidom

numberSplitter = re.compile('\d+|\D+')

def removeElementTags(element, parent): #turn "text <el>text1</el> text2" into "text text1 text2"
    for child in parent.getElementsByTagName(element):
        parent.replaceChild(child.firstChild, child)
def deleteElements(element, parent): #turn "text <el>text1</el> text2" into "text text2"
    for child in parent.getElementsByTagName(element):
        parent.removeChild(child)
def choose(choice):
    found = False
    choices = {'sic': 'corr', 'orig': 'reg', 'abbr': 'expan', 'seg': 'seg'} # given the choose tag, take the second one of the options (value in this dictionary)
    for ch in choices:
        if ch in [child.localName for child in choice.childNodes]:
            found = True
            if ch == 'seg':
                choice.removeChild(choice.firstChild)
                removeElementTags('seg', choice)
            else:
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
    punct = u'“̈҃ⸯ·҇!#$%&=\'()*+,-.:;?@[\\]^_`{|}~”̏′'
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
    output = word[0]
    for index, char in enumerate(word):
        if index > 0:
            if word[index] == word[index-1]:
                continue
            output += char
    return output

def truncate(word): #cut down to at most 4 characters
    return word.replace(' ', '')[:4]

digits = {'1': u'а', '2': u'в', '3': u'г', '4': u'д', '5': u'е', '6': u'ѕ', '7': u'ӡ', '8': u'і', '9': u'ѳ'}
tens = {'1': u'і', '2': u'к', '3': u'л', '4': u'м', '5': u'н', '6': u'ѯ', '7': u'о', '8': u'п', '9': u'ч'}
hundreds = {'1': u'р', '2': u'с', '3': u'т', '4': u'у', '5': u'ф', '6': u'х', '7': u'ѱ', '8': u'ѡ', '9': u'ц'}

def cyrrilizeNumber(num):
    num = num[::-1]
    c = 0
    cyr = ''
    for char in num:
        c += 1
        if not char == '0':
            if c == 1:
                cyr += digits[char]
            elif c == 2:
                cyr += tens[char]
            elif c == 3:
                cyr += hundreds[char]
            elif c == 4:
                cyr += digits[char]
                cyr += u'҂'
            elif c == 5:
                cyr += u'⃝'
                cyr += digits[char]
    return cyr[::-1]


def getNumber(subpart): #generate u values from filename
    if not '-' in subpart:
        for char in subpart:
            if char == '0':
                continue
            startfrom = subpart.index(char)
            break
        try:
            return subpart[startfrom:]
        except UnboundLocalError:
            return '0'
    else:
        return '/'.join([getNumber(i) for i in subpart.split('-')])

def parseName(f): #generate u values from filename
    distance = len(f.split('.')[-1])
    f = f[:-distance].split('_')
    return ','.join([getNumber(i) for i in f[1:]])

def Round(n):
    return str("{0:.2f}".format(n))

def updateProgressBar(scriptName, percentage):
    width = 20
    done = width * int(percentage)/100
    splitUp = scriptName.split('.')
    if len(splitUp[0]) > 10:
        scriptName = splitUp[0][:10] + '~.py'
    sys.stdout.write('\r' + scriptName + '\t[' + done * '*' + (width-done) * ' ' + ']\t' + Round(percentage) + '%')
    sys.stdout.flush()
    

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
    sVowels = [v.firstChild.nodeValue for v in specialVowels]
    wlist = []
    for i in list(splitTagsFromText(w.toxml())):
        if not i.startswith('<'):
            wlist.append(i)
    word = stripPunct(''.join(wlist)).strip()
    if len(word) == 0:
        return 'PUNC'
    splitNumbers = re.findall(numberSplitter, word)
    if len(splitNumbers) > 1 or splitNumbers[0].isdigit():
        temp = []
        for group in splitNumbers:
            if group.isdigit():
                group = cyrrilizeNumber(group)
            temp.extend(group)
        word = ''.join(temp)

# apply rules as specified in soundex-rules.xml
    
    word = applyRule(word, manyToOne)
    word = applyRule(word, oneToMany)
    word = applyRule(word, oneToOne)
    if len(word) < 3:
        if len(word) == 2 and word[1] in sVowels:
            word = word[0]
        return word
    
# entirely eliminating vowels in the special category from all words
    temp = word[0]
    for char in word[1:]:
        for vowel in specialVowels:
            if not char == vowel:
                temp += char
    word = temp
    
# degeminate words, get rid of noninitial vowels
    newWord = word[0] # Keep the first character even if it's a vowel
    degeminated = degeminate(word)
    for char in degeminated[1:]: #Append only consonants starting at the char in position 1
        if not char in vowelList:
            newWord += char
    return truncate(newWord)
