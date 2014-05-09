import datetime, codecs, os, Preprocessing, shutil, sys, xml.dom.minidom as minidom

startTimePP = datetime.datetime.now()
os.chdir(os.path.abspath(os.path.dirname(__file__)))
args = sys.argv

assert len(args) == 3, "Expected exactly 2 arguments!\n\n-i followed by input directory path"
assert '-i' in args and os.path.exists(args[args.index('-i')+1]), "Invalid input directory"

path = args[args.index('-i')+1]
xmls = filter(lambda x: str(x.split('.')[len(x.split('.'))-1]) == 'xml' , os.listdir(path))
c = 0
x = len(xmls)
def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)
 
    previous_row = xrange(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def isBlank(node):
    return node.getAttribute('n') == ''

os.chdir(path)
if os.path.exists('Postprocessed'):
    shutil.rmtree('Postprocessed')
os.mkdir('Postprocessed')

print
for afile in xmls:

    c += 1
    #Preprocessing.updateProgressBar('Postprocessing.py', float(100)*c/x)
    doc = minidom.parse(os.path.join(path, afile))
    blocks = doc.getElementsByTagName('block')
    tokens = doc.getElementsByTagName('token')
    blanks = [token for token in tokens if token.getAttribute('n') == '']
    print blanks
    if blanks:
        #generate dictionary of witness to its token nodes for each row
        column1Toks = blocks[0].getElementsByTagName('token')
        wit2toks = {}
        for token in column1Toks:
            wit = token.getAttribute('witness')
            row = [token for token in doc.getElementsByTagName('token') if token.nodeType == 1 and token.getAttribute('witness') == wit]
            wit2toks[wit] = row
            for (wit, row) in wit2toks.items():
            #generate list of lists of sequences of empty tokens
            fin = []
            temp = []
            for tokenNode in row:
                if isBlank(tokenNode):
                    temp.append(tokenNode)
                    if int(tokenNode.parentNode.getAttribute('n')) == len(row)-1:
                        fin.append(temp)
                        temp = []
                elif temp:
                    fin.append(temp)
                    temp = []
            column2lev = {}
            for i in fin:
                nothingBefore = False
                column2words = {}
                for ind, j in enumerate(i): 
                    if ind == 0:
                        #dealing with the first blank in a sequence of N
                        PCID = int(j.parentNode.getAttribute('n'))-1
                        if PCID == -1:
                            nothingBefore = True #no previous column, aka we're in the first one
                            continue
                        previousColumn = [block for block in blocks if int(block.getAttribute('n')) == PCID][0].getElementsByTagName('token')
                        previousWordNode = [tok for tok in previousColumn if tok.getAttribute('witness') == wit][0]
                        previousWords = set([w.getAttribute('n') for w in previousColumn if w.getAttribute('n') not in [previousWordNode.getAttribute('n'),'']])
                        if previousWords:
                            column2words[PCID] = previousWords
                        else:
                            continue
                    currentToks = j.parentNode.getElementsByTagName('token')
                    currentWords = set([w.getAttribute('n') for w in currentToks if w.getAttribute('n') != ''])
                    column2words[int(j.parentNode.getAttribute('n'))] = currentWords
                if column2words and not nothingBefore:
                    for k in column2words:
                        column2lev[k] = min([levenshtein(previousWordNode.getAttribute('n'), w) for w in column2words[k]])
                    smallestEditDistance = min(column2lev.values())
                    for l in column2lev:
                        if column2lev[l] == smallestEditDistance:
                            moveTo = l
                            break
                    for block in blocks:
                        if int(block.getAttribute('n')) == moveTo:
                            tokenList = block.getElementsByTagName('token')
                            moving = [tok for tok in tokenList if tok.getAttribute('witness') == previousWordNode.getAttribute('witness')][0]
                            #effectively duplicate the node being moved.
                            block.replaceChild(previousWordNode.cloneNode(True), moving) 
                            #iteratively delete all of old node's children (text and/or elements)
                            for child in previousWordNode.childNodes:
                                previousWordNode.removeChild(child)
                            #set its @n to blank. Technically, no reason to do this, but in case we do more postprocessing, will be necessary.
                            previousWordNode.setAttribute('n', '')
    doc.writexml(codecs.open(os.path.join(path, 'Postprocessed', afile), 'w', 'utf-8'))
