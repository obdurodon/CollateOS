import datetime, os, subprocess, sys
startTimeWP = datetime.datetime.now()
curDir = os.getcwd()
os.chdir(os.path.dirname(__file__))
args = sys.argv
script = args[1]
In = os.path.join(curDir, args[args.index('-i')+1])

def checkStatus(p):
    if p != 0:
        sys.exit()
        
print '\nPassing command: python xmltojson.py -i ' + In + '\n'
p = subprocess.Popen(['python', 'xmltojson.py', '-i', In]).wait()
checkStatus(p)

if '-new' in args:
    print '\nPassing command: python runCollatex.py -i ' + os.path.abspath(In) + ' -new\n'
    p = subprocess.Popen(['python', 'runCollatex.py', '-i', os.path.abspath(In), '-new']).wait()
    checkStatus(p)
    print '\nPassing command: python jsontoxml.py -i ' + os.path.join(os.path.abspath(In), 'collatexoutput') + '\n'
    p = subprocess.Popen(['python', 'jsontoxml.py', '-i', os.path.join(os.path.abspath(In), 'collatexoutput')]).wait()
    checkStatus(p)
else:
    print '\nPassing command: python runCollatex.py -i ' + os.path.abspath(In) + '\n'
    p = subprocess.Popen(['python', 'runCollatex.py', '-i', os.path.abspath(In)]).wait()
    print '\nPassing command: python jsontoxml.py -i ' + os.path.abspath(In) + '\n'
    p = subprocess.Popen(['python', 'jsontoxml.py', '-i', os.path.abspath(In)]).wait()
    checkStatus(p)
print '\nPassing command: python Preprocessing.py -i', os.path.join(os.path.abspath(In), 'collatexoutput') + '\n'
p = subprocess.Popen(['python', 'Postprocessing.py', '-i', os.path.join(os.path.abspath(In), 'collatexoutput')]).wait()
checkStatus(p)
print '\nTook', datetime.datetime.now()-startTimeWP, 'to execute wrapper.py'
