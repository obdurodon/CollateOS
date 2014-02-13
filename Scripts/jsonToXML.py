import codecs, json, xml.dom.minidom as minidom
data = json.loads(open('output.json', 'r').read())
nameToNumber = {number:name for number, name in enumerate(data['witnesses'])}
def normalChars(l):
    return l.replace('&lt;', '<').replace('&gt;','>').replace('&quot;', '"')
with codecs.open('XMLObjects.xml','w') as out:
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
            if token:
                textNodeValue = token[0]['t']
                normalizedAttrValue = token[0]['n']
            else:
                textNodeValue = ''
                normalizedAttrValue = ''
            tokenElement.appendChild(doc.createTextNode(textNodeValue))
            tokenElement.setAttribute('n', normalizedAttrValue)
            tokenElement.setAttribute('witness', nameToNumber[number])
            blockElement.appendChild(tokenElement)
            number += 1
        witnessElement.appendChild(blockElement)
    for ln in doc.toprettyxml().split('\n'):
        out.write(normalChars(ln).encode('utf-8') + '\n')
