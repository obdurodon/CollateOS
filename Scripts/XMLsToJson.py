# -*- coding: utf-8 -*-

import datetime, json, os, Preprocessing, sys, xml.dom.minidom as minidom

startTime = datetime.datetime.now()

args = sys.argv

assert 5 <= len(args) <= 6, "Expected 4 or 5 arguments! \n\n-i followed by input directory path\n-o followed by output file path\noptional debug flag"
assert '-i' in args and os.path.exists(args[args.index('-i')+1]), "Invalid input directory"
assert '-o' in args and not args.index('-o') == len(args)-1, "No output file path provided"

path = args[args.index('-i')+1]
jsonFileName = os.path.join(os.getcwd(), args[args.index('-o')+1])

debug = False
if 'debug' in args:
    debug = True
    html = open('debug.html', 'w')
    html.write('<html><head><title>Debugging at ' + str(datetime.datetime.now()) + '</title><meta http-equiv="content-type" content="application/xhtml+xml; charset=UTF-8" /></head><body>')

xmls = filter(lambda x: str(x.split('.')[len(x.split('.'))-1]) == 'xml' , os.listdir(path))
root = {}
alldocs = []
l = len(xmls)
count = 0
for afile in xmls:
    count += 1
    print 'XMLsToJSON.py: Processing', afile, 'file', count, 'out of', l 
    docLevel = {}
    docLevel['id'] = afile
    tokenList = []
    if debug:
        html.write('<h2>' + afile + '</h2><table border = "1"><th>Original<th>Conflated</th>')
    ws = minidom.parse(os.path.join(path, afile)).getElementsByTagName('w')
    words = []
    for w in range(len(ws)):
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
        token['u'] = currentWord.getAttribute('n')
        if debug:
            html.write('<tr><td>' + currentWord.toxml().encode('utf-8') + '</td><td>' + c.encode('utf-8') + '</td></tr>')
        words.append(c)
        tokenList.append(token)
    if debug:
        html.write('</table>')
    docLevel['tokens'] = tokenList
    alldocs.append(docLevel)
root['witnesses'] = alldocs
if debug:
    html.write('</body></html>')
    print 'debug file written to', os.path.join(os.getcwd(), html.name)
    html.close()
with open(os.path.join(path, jsonFileName), 'w') as Json:
    Json.write(json.dumps(root, ensure_ascii=False).encode('utf-8'))
print 'Took', datetime.datetime.now()-startTime, 'to execute XMLsToJSON.py'
