import xml.dom.minidom as minidom

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
 
    # len(s1) >= len(s2)
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

f = minidom.parse(r'../pvl/blocks/collatexOutput/0165_0009_0002.xml')
blocks = f.getElementsByTagName('block')

for block in xrange(len(blocks)):
	tokens = blocks[block].getElementsByTagName('token')
	for token in tokens:
		if token.getAttribute('n') == '':
			previousWords = blocks[block-1].getElementsByTagName('token')
			currentWords = blocks[block].getElementsByTagName('token')
			wit = token.getAttribute('witness')
			previousWord = [word for word in previousWords if word.getAttribute('witness') == wit][0].getAttribute('n')
			previousNs = set([w.getAttribute('n') for w in previousWords if w.getAttribute('n') != previousWord])
			currentNs = set([w.getAttribute('n') for w in currentWords if w.getAttribute('n') != ''])
			if len(previousNs) > 0:
				print '\npast:'
				for w in previousNs:
					print w, levenshtein(previousWord, w)
				print '\ncur:'
				for w in currentNs:
					print w, levenshtein(previousWord, w)
