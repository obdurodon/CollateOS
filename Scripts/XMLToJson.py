# -*- coding: utf-8 -*-
#parsing a single xml file, like the pavlova project, split into blocks. Output written into the same folder. Presumably deleted afterwards downthe pipeline.

import datetime, json, os, Preprocessing, sys, xml.dom.minidom as minidom
startTime = datetime.datetime.now()

args = sys.argv

assert len(args) == 3, "Expected 4 arguments exactly! \n\n-i followed by input directory path"
assert '-i' in args and os.path.exists(args[args.index('-i')+1]), "Invalid input directory"

path = args[args.index('-i')+1]
xmls = filter(lambda x: str(x.split('.')[len(x.split('.'))-1]) == 'xml' , os.listdir(path))
l = len(xmls)
count = 0
for afile in xmls:
    count += 1
    print 'XMLToJSON.py: Processing', afile, 'file', count, 'out of', l 
    root = {}
    alldocs = []
    rdgs = minidom.parse(os.path.join(path, afile)).getElementsByTagName('rdg')
    for rdg in rdgs:
        docLevel = {}
        docLevel['id'] = rdg.getAttribute('wit')
        tokenList = []
        ws = rdg.getElementsByTagName('w')
        words = []
        for w in range(len(ws)):
            currentWord = ws[w]
            previousWord = ''
            try:
                previousWord = ws[w-1]
            except IndexError:
                pass
            token = {}
            token['t'] = currentWord.toxml()[3:-4]
            c = Preprocessing.conflate(currentWord)
##            if c == Preprocessing.conflate(previousWord):
##                c += '1' # tag '1' to the end of a wod that we suspect is repeated in the manuscript.
            token['n'] = c
            token['u'] = currentWord.getAttribute('n')
            words.append(c)
            tokenList.append(token)
        docLevel['tokens'] = tokenList
        alldocs.append(docLevel)
    root['witnesses'] = alldocs
    with open(os.path.join(path, afile[:-3] + 'json'), 'w') as Json:
        Json.write(json.dumps(root, ensure_ascii=False).encode('utf-8'))
print 'Took', datetime.datetime.now()-startTime, 'to execute XMLToJSON.py'
