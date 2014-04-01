import datetime, os, shutil, sys
startTimeRC = datetime.datetime.now()
os.chdir(os.path.abspath(os.path.dirname(__file__)))
args = sys.argv
assert 3 <= len(args) <= 4, "Expected 2 or 3 arguments! \n\n-i followed by input directory path\n-new if opting not to overwrite the existing JSONs"
assert '-i' in args and os.path.exists(args[args.index('-i')+1]), "Invalid input directory"

os.chdir('../collatex-tools-1.5.2-SNAPSHOT/bin')
path = args[args.index('-i')+1]
overwrite = True if not '-new' in args else False
jsons = filter(lambda x: str(x.split('.')[len(x.split('.'))-1]) == 'json' , os.listdir(path))

l = len(jsons)
c = 0
if os.path.exists(os.path.join(path, 'collatexOutput')):
    shutil.rmtree(os.path.join(path, 'collatexOutput')) # delete any old output

if not overwrite:
    os.mkdir(os.path.join(path, 'collatexOutput'))

    
for afile in jsons:
    if overwrite:
        outpath = os.path.join(path, afile)
    else:
        outpath = os.path.join(path, 'collatexOutput', afile)
    c += 1
    print 'runCollatex.py: Processing', afile, 'file', c, 'out of', l
    os.popen(os.path.join('.', 'collatex') + ' -t -l -lt 1 -o ' + outpath + ' ' + os.path.join(path,afile))
        
print 'Took', datetime.datetime.now()-startTimeRC, 'to execute runCollatex.py'
