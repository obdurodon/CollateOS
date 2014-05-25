import codecs, os, sys

args = sys.argv
inPath = args[2]
outPath = inPath[:-4] + '.out.txt'

with codecs.open(inPath, 'r', encoding='utf-8') as t1:
    with codecs.open(outPath, 'w', encoding='utf-8') as t2:
        wordList = [i.split(':')[0].replace('; ', ';').strip().split(';') for i in t1.readlines()]
        for i in wordList:
            for k in i:
                for j in wordList:
                    for l in j:
                        if l == k and i != j:
                            for m in j:
                                i.append(m)
                            wordList.remove(j)
                            continue
        for i in wordList:
            t2.write(';'.join(i) + '\n')
