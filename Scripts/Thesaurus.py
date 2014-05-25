import codecs,datetime, os, Preprocessing, sys, xml.dom.minidom as minidom

startTimeTS = datetime.datetime.now()
args = sys.argv

path = args[args.index('-i') + 1]
xmls = filter(lambda x: str(x.split('.')[len(x.split('.'))-1]) == 'xml' , os.listdir(path))

def allSame(b):
    toks = b.getElementsByTagName('token')
    nonEmpty = [tok.getAttribute('n') for tok in toks if tok.getAttribute('n') != '']
    if len(nonEmpty) == len(toks) and len(set(nonEmpty)) == 1:
        return True
    return False

def getAllToks(b):
    toks = b.getElementsByTagName('token')
    return [tok.getAttribute('n') for tok in toks if tok.getAttribute('n') != '']

c = 0
l = len(xmls)
thes = {}
for afile in xmls:
    c += 1
    Preprocessing.updateProgressBar('Thesaurus', float(100)*c/l)
    doc = minidom.parse(os.path.join(path, afile))
    #print os.path.join(path, afile)
    blocks = doc.getElementsByTagName('block')
    for b in range(len(blocks)):
        #print blocks[b].toxml().encode('ascii', 'replace')
        if not len(set([tok.getAttribute('n') for tok in blocks[b].getElementsByTagName('token') if not tok.getAttribute('n') == ''])) == 1 and len(blocks) >= 3:
            if b == 0 and allSame(blocks[1]):
                thes[Preprocessing.parseName(afile)] = set(getAllToks(blocks[0]))
            elif b == len(blocks)-1 and allSame(blocks[len(blocks)-2]):
                thes[Preprocessing.parseName(afile)] = set(getAllToks(blocks[len(blocks)-1]))
            elif allSame(blocks[b-1]) and allSame(blocks[b+1]):
                thes[Preprocessing.parseName(afile)] = set(getAllToks(blocks[b]))

inverse = {}
for k, v in thes.items():
    v = '; '.join(v)
    inverse[v] = inverse.get(v, [])
    inverse[v].append(k)



with codecs.open(r'c:/users/minas/desktop/thes.txt', 'w', encoding='utf-8') as t:
    for i in inverse:
        t.write(i + ' : ' + ', '.join(inverse[i]) + '\n')

with codecs.open(r'c:/users/minas/desktop/thes.txt', 'r', encoding='utf-8') as t1:
    with codecs.open(r'c:/users/minas/desktop/thes2.txt', 'w', encoding='utf-8') as t2:
        wordList = [i.split(':')[0].replace('; ', ';').strip().split(';') for i in t1.readlines()]
        for i in wordList:
            l = ';'.join(i) + '\n'
            t2.write(l)
