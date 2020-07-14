'''
Authur : Quazi Rabbi
Objective : update the commit number in __init__.py -> __version__ = 'Major.Minor.Patch.CommitNumber' ( i.e - __version__ = '1.1.0.12'  )
How it works :  1. runs git rev-list command to get commit number
                2. find the module name, which must should be same as main directory name .../documents/myModule/myModule/__init__.py
                    if the module name is not same as main directory name - then run python versionUpdate.py myModule
                3. reads the __version__ in __init__.py and replaces only the CommitNumber

Additional Step - to run as git pre-commit hook - add a file 'pre-commit' (no file extension) in .git->hooks with the following lines :
                #!/bin/sh
                # To enable this hook, rename this file to "pre-commit".

                python3 PyInstaller_Build_Scripts\\versionUpdate.py
'''

import sys,os,re,subprocess
from tempfile import mkstemp
from shutil import move, copymode

def getCommitNumber():
    '''
    Returns the commit number of the git repo  
    '''
    out,_ = subprocess.Popen(['git', 'rev-list', 'HEAD', '--count'], 
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT).communicate()
    if out[:5] == 'fatal':
        out='0'
    return str(int(out)+1)

def updateVersion(commitNumber,moduleName=None):
    '''
    Takes the commitNumber as ascii string
    Updates the __version__ number in the module
    '''
    if not moduleName:
        moduleName = os.getcwd().split('\\')[-1]
    os.chdir(moduleName)
    file_name = '__init__.py'
    
    #Create a temp file
    fh, abs_path = mkstemp()
    new_version = None
    with os.fdopen(fh,'w') as new_file:
        with open(file_name,'r') as old_file:
            for line in old_file:
                if '__version__' in line:
                    try:
                        old_version = re.findall(r"'(.+?)'",line)[0]
                        version = old_version.split('.')
                        version[-1] = commitNumber
                        new_version = ".".join(version)
                        new_file.write(line.replace(old_version, new_version))
                    except:
                        new_file.write(line)
                else:
                    new_file.write(line)
    
    #Copy the file permissions from the old file to the new file
    copymode(file_name, abs_path)
    #Remove original file
    os.remove(file_name)
    #Move new file
    move(abs_path, file_name)

    try:
        subprocess.call(['git', 'tag', f'v{new_version}'])
    except:
        pass
    subprocess.call(['git', 'add', '__init__.py'])
    

if __name__ == '__main__':
    print('Version Update in module started')
    moduleName = sys.argv[-1]
    if '.py' in moduleName:
        updateVersion(getCommitNumber())
    else:
        updateVersion(getCommitNumber(),moduleName)
    print('Version Update in module finished')
        
    