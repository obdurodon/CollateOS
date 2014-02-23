import datetime, codecs, json, os, sys, xml.dom.minidom as minidom

startTime = datetime.datetime.now()
args = sys.argv
assert len(sys.argv) == 3, "Expected exactly 2 arguments!\n\n-i followed by input directory path"
assert '-i' in args and os.path.exists(args[args.index('-i')+1]), "Invalid input directory"

def normalChars(l):
    return l.replace('&lt;', '<').replace('&gt;','>').replace('&quot;', '"')
path = args[args.index('-i')+1]
jsons = filter(lambda x: str(x.split('.')[len(x.split('.'))-1]) == 'json' , os.listdir(path))
os.chdir(path)
c = 0
l = len(jsons)
couldnt = []
for afile in jsons:
    try:
        c += 1
        print 'Processing', afile, 'file', c, 'out of', l
        data = json.loads(open(afile, 'r').read())
        nameToNumber = {number:name for number, name in enumerate(data['witnesses'])}
        with codecs.open(afile[:-4] + 'xml','w') as out:
            doc = minidom.Document()
            witnessElement = doc.createElement('witnesses')
            doc.appendChild(witnessElement)
            for block in data['table']:
                blockElement = doc.createElement('block')
                number = 0
                for token in block:
                    tokenElement = doc.createElement('token')
                    tokenElement.setAttributeNode(doc.createAttribute('n'))
                    tokenElement.setAttributeNode(doc.createAttribute('witness'))
                    tokenElement.setAttributeNode(doc.createAttribute('u'))
                    if token:
                        textNodeValue = token[0]['t']
                        normalizedAttrValue = token[0]['n']
                        unitValue = token[0]['u']
                    else:
                        textNodeValue = ''
                        normalizedAttrValue = ''
                        unitValue = ''
                    tokenElement.appendChild(doc.createTextNode(textNodeValue))
                    tokenElement.setAttribute('n', normalizedAttrValue)
                    tokenElement.setAttribute('u', unitValue)
                    tokenElement.setAttribute('witness', nameToNumber[number])
                    blockElement.appendChild(tokenElement)
                    number += 1
                witnessElement.appendChild(blockElement)
            for ln in doc.toprettyxml().split('\n'):
                out.write(normalChars(ln).encode('utf-8') + '\n')
    except:
        couldnt.append(afile)
print 'Took', datetime.datetime.now()-startTime, 'to execute JSONToXML.py'
print 'failed on', len(couldnt), 'files:', couldnt
