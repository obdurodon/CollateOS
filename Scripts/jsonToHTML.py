import json
data = json.loads(open('output.json', 'r').read())
out = open('testOut.html', 'w')
out.write('<html xmlns="http://www.w3.org/1999/xhtml">\n<head>\n<title>test</title>\n<link href="http://www.obdurodon.org/css/style.css" rel="stylesheet" type="text/css"/>\n<link href="css/scholia.css" rel="stylesheet" type="text/css"/>\n<link href="css/collate.css" rel="stylesheet" type="text/css"/>\n<meta http-equiv="content-type" content="application/xhtml+xml; charset=UTF-8"/>\n</head>\n<body>\n<table>')
for wName in data['witnesses']:
    out.write('\n<tr><td>' + wName.encode('utf-8') + '</td></tr>')
out.write('\n</table>')
for wordList in data['table']:
    out.write('\n<table>')
    for word in wordList:
        if word:
            out.write('\n<tr><td>' + word[0]['t'].encode('utf-8') + '</td></tr>')
        else:
            out.write('\n<tr><td>&#xa0;</td></tr>')
    out.write('\n</table>')
out.write('\n</body>\n</html>')
out.close()
