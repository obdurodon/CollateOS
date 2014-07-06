import datetime
startTime = datetime.datetime.now()
import sys
sys.stdout.write('\nImporting packages...')
import codecs
import gc
import json
import os
import sys
import xml.dom.minidom as minidom

sys.path.append(os.path.join(os.getcwd(), 'collatex/collatex-pythonport'))
LAUNCHED_FROM = os.getcwd()
RESOURCE_HOME = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
COLLATEX_PATH = 'collatex/collatex-pythonport'
sys.path.append(os.path.join(RESOURCE_HOME, COLLATEX_PATH))
FLUSH = 100



from collatex import *
import Preprocessing
args = sys.argv
inputPath = args[args.index('-i') + 1]
if '-f' in args:
    FLUSH = int(args[args.index('-f') + 1])

sys.stdout.write(' Done.')
sys.stdout.write('\nParsing the XML...')
doc = minidom.parse(os.path.join(LAUNCHED_FROM, inputPath))
sys.stdout.write(' Done.\n')
apps = doc.getElementsByTagName('app')
l = len(apps)
c = 0

def createJsonRepresentation(app):
    unit = app.parentNode.parentNode.parentNode.getAttribute('n') + ',' + app.parentNode.parentNode.getAttribute('n')
    root = {}
    allWits = []
    rdgs = [el for el in app.childNodes if el.nodeType == 1]
    for rdg in rdgs:
        appLevel = {}
        appLevel['id'] = rdg.getAttribute('wit')
        tokenList = []
        ws = rdg.getElementsByTagName('w')
        for ind, w in enumerate(ws):
            if not 3 in [child.nodeType for child in w.childNodes]:
                continue
            currentWord = w
            if ind == 0:
                previousWord = ''
            else:
                previousWord = ws[ind-1]
            token = {}
            token['t'] = currentWord.toxml()[8 + len(w.getAttribute('n')):-4]
            token['n'] = Preprocessing.conflate(currentWord)
            token['u'] = unit
            tokenList.append(token)
        appLevel['tokens'] = tokenList
        allWits.append(appLevel)
    root['witnesses'] = allWits
    return json.loads(json.dumps(root))

def normalChars(l):
    return l.replace('&lt;', '<').replace('&gt;','>').replace('&quot;', '"')

def createColumn(Json):
    with codecs.open('testDumpJSON.txt', 'w') as dump1:
        dump1.write(Json.encode('utf-8') + '\n\n')
    data = json.loads(Json)
    print data['witnesses']
    for number, name in enumerate(data['witnesses']):
        print number, name, type(number), type(name)
    nameToNumber = {number:name for number, name in enumerate(data['witnesses'])}
    temp = minidom.Document()
    root = temp.createElement('column')
    temp.appendChild(root)
    for block in data['table']:
        blockElement = temp.createElement('block')
        number = 0
        for token in block:
            tokenElement = temp.createElement('token')
            tokenElement.setAttributeNode(doc.createAttribute('n'))
            tokenElement.setAttributeNode(doc.createAttribute('witness'))
            #tokenElement.setAttributeNode(doc.createAttribute('u'))
            textNodeValue = token[0]['t']
            if textNodeValue != '-':
                normalizedAttrValue = token[0]['n']
            else:
                normalizedAttrValue = ''
            tokenElement.appendChild(doc.createTextNode(textNodeValue))
            tokenElement.setAttribute('n', normalizedAttrValue)
            #tokenElement.setAttribute('u', unitValue)
            tokenElement.setAttribute('witness', nameToNumber[number])
            blockElement.appendChild(tokenElement)
            number += 1
        root.appendChild(blockElement)
    with codecs.open('testDumpXML.txt', 'w') as dump:
        dump.write(root.toxml().encode('utf-8') + '\n\n')




for app in apps:
    c += 1
    Preprocessing.updateProgressBar('Collation', float(100)*c/l)
    collationResults = collate_pretokenized_json(createJsonRepresentation(app), 'json')
    createColumn(collationResults)
    with codecs.open('testDump.txt', 'w') as dump:
        dump.write(collationResults.encode('utf-8') + '\n\n')
    if c % FLUSH == 0:
        gc.collect()
    if c == 100:
        break
print 'Took', datetime.datetime.now() - startTime, 'to execute.'
