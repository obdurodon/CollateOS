import re
witRegex = re.compile('^<.*?>(.*)</.*?>$')
stuff = '<lav>blah</lav>'
print(witRegex.match(stuff).group(1))