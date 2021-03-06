# -*- coding: utf-8 -*-
#parsing a single xml file, like the pavlova project, split into blocks. Output written into the same folder. Presumably deleted afterwards downthe pipeline.

import datetime, json, os, Preprocessing, sys, xml.dom.minidom as minidom
os.chdir(os.path.abspath(os.path.dirname(__file__)))
args = sys.argv
assert len(args) == 3, "Expected 4 arguments exactly! -i followed by input directory path"
assert '-i' in args and os.path.exists(args[args.index('-i')+1]), "Invalid input directory"

path = args[args.index('-i')+1]

xmls = filter(lambda x: str(x.split('.')[len(x.split('.'))-1]) == 'xml' , os.listdir(path))
l = len(xmls)
count = 0
print
for afile in xmls:
    count += 1
    Preprocessing.updateProgressBar('XMLtoJSON.py', float(100)*count/l)
    unit = Preprocessing.parseName(afile) 
    root = {}
    alldocs = []
    rdgs = [el for el in minidom.parse(os.path.join(path, afile)).getElementsByTagName('*') if el.localName in ['lem', 'rdg']]
    for rdg in rdgs:
        docLevel = {}
        docLevel['id'] = rdg.getAttribute('wit')
        tokenList = []
        ws = rdg.getElementsByTagName('w')
        words = []
        for w in range(len(ws)):
            if not 3 in [child.nodeType for child in ws[w].childNodes]: #checking presence of text nodes inside the w
                continue
            currentWord = ws[w]
            previousWord = ''
            try:
                previousWord = ws[w-1]
            except IndexError:
                pass
            token = {}
            token['t'] = currentWord.toxml()[8 + len(ws[w].getAttribute('n')):-4]
            c = Preprocessing.conflate(currentWord)
            token['n'] = c
            token['u'] = unit
            words.append(c)
            tokenList.append(token)
        docLevel['tokens'] = tokenList
        alldocs.append(docLevel)
    root['witnesses'] = alldocs
    with open(os.path.join(path, afile[:-3] + 'json'), 'w') as Json:
        Json.write(json.dumps(root, ensure_ascii=False).encode('utf-8'))
