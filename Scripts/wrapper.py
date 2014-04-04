import datetime, os, subprocess, sys
startTimeWP = datetime.datetime.now()
curDir = os.getcwd()
os.chdir(os.path.dirname(__file__))
args = sys.argv
script = args[1]
In = os.path.join(curDir, args[args.index('-i')+1])

print args

if script.lower() == 'xmltojson.py':
    sameDir = True
    print 'Passing command: python xmltojson.py -i ' + In
    subprocess.Popen(['python', script, '-i', In]).wait()
elif script.lower() == 'xmlstojson.py':
    sameDir = False
    Out = args[args.index('-o')+1]
    print 'Passing command: python xmlstojson.py -i ' + In + ' -o ' + Out
    subprocess.Popen(['python', script, '-i', In, '-o', Out]).wait()
else:
    raise Exception("Input script incorrect")
if '-new' in args:
    if sameDir:
        print 'Passing command: python runCollatex.py -i ' + os.path.abspath(In) + ' -new'
        subprocess.Popen(['python', 'runCollatex.py', '-i', os.path.abspath(In), '-new']).wait()
        print 'Passing command: python jsontoxml.py -i ' + os.path.join(os.path.abspath(In), 'collatexoutput')
        subprocess.Popen(['python', 'jsontoxml.py', '-i', os.path.join(os.path.abspath(In), 'collatexoutput')]).wait()
    else:
        print 'Passing command: python runCollatex.py -i ' + os.path.abspath(os.path.dirname(Out)) + ' -new'
        subprocess.Popen(['python', 'runCollatex.py', '-i', os.path.abspath(os.path.dirname(Out)), '-new']).wait()
        print 'Passing command: python jsontoxml.py -i ' + os.path.join(os.path.abspath(Out), 'collatexoutput')
        subprocess.Popen(['python', 'jsontoxml.py', '-i', os.path.join(os.path.abspath(Out), 'collatexoutput')]).wait()
else:
    if sameDir:
        print 'Passing command: python runCollatex.py -i ' + os.path.abspath(In)
        subprocess.Popen(['python', 'runCollatex.py', '-i', os.path.abspath(In)]).wait()
        print 'Passing command: python jsontoxml.py -i ' + os.path.abspath(In)
        subprocess.Popen(['python', 'jsontoxml.py', '-i', os.path.abspath(In)]).wait()
    else:
        print 'Passing command: python runCollatex.py -i ' + os.path.abspath(os.path.dirname(Out))
        subprocess.Popen(['python', 'runCollatex.py', '-i', os.path.abspath(os.path.dirname(Out))]).wait()
        print 'Passing command: python jsontoxml.py -i ' + os.path.abspath(Out)
        subprocess.Popen(['python', 'jsontoxml.py', '-i', os.path.abspath(Out)]).wait()
print 'Took', datetime.datetime.now()-startTimeWP, 'to execute wrapper.py'
