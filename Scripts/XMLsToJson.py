# -*- coding: utf-8 -*-

import datetime, json, os, Preprocessing, sys, xml.dom.minidom as minidom

startTimeX2J = datetime.datetime.now()
os.chdir(os.path.abspath(os.path.dirname(__file__)))
args = sys.argv

assert len(args) == 5, "Expected 4 arguments! \n\n-i followed by input directory path\n-o followed by output file path"
assert '-i' in args and os.path.exists(args[args.index('-i')+1]), "Invalid input directory"
assert '-o' in args and not args.index('-o') == len(args)-1, "No output file path provided"

path = args[args.index('-i')+1]
jsonFileName = os.path.join(os.getcwd(), args[args.index('-o')+1])

xmls = filter(lambda x: str(x.split('.')[len(x.split('.'))-1]) == 'xml' , os.listdir(path))
root = {}
alldocs = []
l = len(xmls)
count = 0
for afile in xmls:
    count += 1
    print 'XMLsToJSON.py: Processing', afile, 'file', count, 'out of', l
    unit = Preprocessing.parseName(afile) 
    docLevel = {}
    docLevel['id'] = afile
    tokenList = []
    if debug:
        html.write('<h2>' + afile + '</h2><table border = "1"><th>Original<th>Conflated</th>')
    ws = minidom.parse(os.path.join(path, afile)).getElementsByTagName('w')
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
        token['t'] = currentWord.toxml()[8+len(currentWord.getAttribute('n')):-4]
        c = Preprocessing.conflate(currentWord)
        if c == Preprocessing.conflate(previousWord):
            c += '1' # tag '1' to the end of a wod that we suspect is repeated in the manuscript.
        token['n'] = c
        token['u'] = unit
        words.append(c)
        tokenList.append(token)
    docLevel['tokens'] = tokenList
    alldocs.append(docLevel)
root['witnesses'] = alldocs
with open(os.path.join(path, jsonFileName), 'w') as Json:
    Json.write(json.dumps(root, ensure_ascii=False).encode('utf-8'))
print 'Took', datetime.datetime.now()-startTimeX2J, 'to execute XMLsToJSON.py'
