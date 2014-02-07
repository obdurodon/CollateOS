import json
data = json.loads(open('output.json', 'r').read())
out = open('testOut.html', 'w')
out.write('<html><head><title>test</title></head><body><table border="1", style="display: inline-block;">')
for wName in data['witnesses']:
    out.write('<tr><td>' + wName.encode('utf-8') + '</td></tr>')
out.write('</table>')
for wordList in data['table']:
    out.write('<table border="1", style="display: inline-block;">')
    for word in wordList:
        if word:
            out.write('<tr><td>' + word[0]['t'].encode('utf-8') + '</td></tr>')
        else:
            out.write('<tr><td></td></tr>')
    out.write('</table>')
out.write('</body></html>')
out.close()
