import datetime, os, subprocess, sys

def checkStatus(p):
    if p != 0:
        sys.exit()

def getDateTime(which):
    timer = datetime.datetime.now()
    if which == 'date':
        n = 0
    elif which == 'time':
        n = 1
    return str(timer).split()[n]

timeLog = []
startTimeWP = datetime.datetime.now()
timeLog.extend('*** ' + str(datetime.datetime.now()).split()[0] + ' ***\n\n')
curDir = os.getcwd()
os.chdir(os.path.dirname(__file__))
args = sys.argv
script = args[1]
In = os.path.join(curDir, args[args.index('-i')+1])            
##print '\nPassing command: python xmltojson.py -i ' + In + '\n'
x2j = datetime.datetime.now()
p = subprocess.Popen(['python', 'xmltojson.py', '-i', In]).wait()
checkStatus(p)
timeLog.extend('Took ' + str(datetime.datetime.now() - x2j) + ' to execute XMLtoJSON.py\n')

if '-new' in args:
##    print '\nPassing command: python runCollatex.py -i ' + os.path.abspath(In) + ' -new\n'
    rc = datetime.datetime.now()
    p = subprocess.Popen(['python', 'runCollatex.py', '-i', os.path.abspath(In), '-new']).wait()
    checkStatus(p)
    timeLog.extend('Took ' + str(datetime.datetime.now() - rc) + ' to execute runCollatex.py\n')
##    print '\nPassing command: python jsontoxml.py -i ' + os.path.join(os.path.abspath(In), 'collatexoutput') + '\n'
    j2x = datetime.datetime.now()
    p = subprocess.Popen(['python', 'jsontoxml.py', '-i', os.path.join(os.path.abspath(In), 'collatexoutput')]).wait()
    checkStatus(p)
    timeLog.extend('Took ' + str(datetime.datetime.now() - j2x) + ' to execute JSONtoXML.py\n')
else:
##    print '\nPassing command: python runCollatex.py -i ' + os.path.abspath(In) + '\n'
    rc = datetime.datetime.now()
    p = subprocess.Popen(['python', 'runCollatex.py', '-i', os.path.abspath(In)]).wait()
    timeLog.extend('Took ' + str(datetime.datetime.now() - rc) + ' to execute runCollatex.py\n')
##    print '\nPassing command: python jsontoxml.py -i ' + os.path.abspath(In) + '\n'
    j2x = datetime.datetime.now()
    p = subprocess.Popen(['python', 'jsontoxml.py', '-i', os.path.abspath(In)]).wait()
    checkStatus(p)
    timeLog.extend('Took ' + str(datetime.datetime.now() - j2x) + ' to execute JSONtoXML.py\n')
##print '\nPassing command: python Preprocessing.py -i', os.path.join(os.path.abspath(In), 'collatexoutput') + '\n'
pp = datetime.datetime.now()
p = subprocess.Popen(['python', 'Postprocessing.py', '-i', os.path.join(os.path.abspath(In), 'collatexoutput')]).wait()
checkStatus(p)
timeLog.extend('Took ' + str(datetime.datetime.now() - pp) + ' to execute Postprocessing.py\n')
timeLog.extend('Total execution time: ' + str(datetime.datetime.now() - startTimeWP) + '\n\n')
print '\n\nTook', datetime.datetime.now()-startTimeWP, 'to execute wrapper.py\n\nFull time log found at timeLog.txt in Scripts directory.'
with open('timeLog.txt', 'w') as timer:
    for i in timeLog:
        timer.write(i)
