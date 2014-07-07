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
def getUnit(app):
    return app.getElementsByTagName('w')[0].getAttribute('n')

def createJsonRepresentation(app):
    unit = getUnit(app)
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

def processColumn(Json, unitValue):
    data = json.loads(Json)
    nameToNumber = {number:name for number, name in enumerate(data['witnesses'])}
    temp = minidom.Document()
    line = temp.createElement('line')
    temp.appendChild(line)
    number = 0
    for block in data['table']:
        blockElement = temp.createElement('block')
        for token in block:
            tokenElement = temp.createElement('token')
            tokenElement.setAttributeNode(doc.createAttribute('n'))
            tokenElement.setAttributeNode(doc.createAttribute('witness'))
            tokenElement.setAttributeNode(doc.createAttribute('u'))
            textNodeValue = token[0]['t']
            if textNodeValue != '-':
                normalizedAttrValue = token[0]['n']
            else:
                textNodeValue = ''
                normalizedAttrValue = ''
            tokenElement.appendChild(doc.createTextNode(textNodeValue))
            tokenElement.setAttribute('n', normalizedAttrValue)
            tokenElement.setAttribute('u', unitValue)
            tokenElement.setAttribute('witness', nameToNumber[number])
            blockElement.appendChild(tokenElement)
        number += 1
        line.appendChild(blockElement)
    return normalChars(line.toxml().encode('utf-8'))

if os.path.exists('output.xml'):
    os.remove('output.xml')
with codecs.open('output.xml', 'a') as out:
    out.write('<collationOutput>')
    for app in apps:
        c += 1
        Preprocessing.updateProgressBar('Collation', float(100)*c/l)
        collationResults = collate_pretokenized_json(createJsonRepresentation(app), 'json')
        out.write(processColumn(collationResults, getUnit(app)))
        if c % FLUSH == 0:
            gc.collect()
    out.write('</collationOutput>')

print '\nTook', datetime.datetime.now() - startTime, 'to execute.'
