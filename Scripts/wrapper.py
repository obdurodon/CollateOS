import datetime, os, subprocess, sys
startTime = datetime.datetime.now()
args = sys.argv
script = args[1]
In = args[args.index('-i')+1]

print args

if script.lower() == 'xmltojson.py':
    sameDir = True
    print 'Passing command: python xmltojson.py -i ' + In
    subprocess.Popen('python xmltojson.py -i ' + In).wait()
elif script.lower() == 'xmlstojson.py':
    sameDir = False
    Out = args[args.index('-o')+1]
    print 'Passing command: python xmlstojson.py -i ' + In + ' -o ' + Out
    subprocess.Popen('python xmlstojson.py -i ' + In + ' -o ' + Out).wait()
else:
    raise Exception("Input script incorrect")
if '-new' in args:
    if sameDir:
        print 'Passing command: python runCollatex.py -i ' + os.path.abspath(In) + ' -new'
        subprocess.Popen('python runCollatex.py -i ' + os.path.abspath(In) + ' -new')
    else:
        print 'Passing command: python runCollatex.py -i ' + os.path.abspath(os.path.dirname(Out)) + ' -new'
        subprocess.Popen('python runCollatex.py -i ' + os.path.abspath(os.path.dirname(Out)) + ' -new')
else:
    if sameDir:
        print 'Passing command: python runCollatex.py -i ' + os.path.abspath(In)
        subprocess.Popen('python runCollatex.py -i ' + os.path.abspath(In))
    else:
        print 'Passing command: python runCollatex.py -i ' + os.path.abspath(os.path.dirname(Out))
        subprocess.Popen('python runCollatex.py -i ' + os.path.abspath(os.path.dirname(Out)))
print 'Took', datetime.datetime.now()-startTime, 'to execute wrapper.py'
