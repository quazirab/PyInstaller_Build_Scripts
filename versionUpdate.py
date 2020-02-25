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
    line = None
    with open('__init__.py','r') as file:
        line = file.read()
        version = re.findall(r"'(.+?)'",line)[-1]
        version = version.split('.')
        version[-1] = commitNumber
        version = ".".join(version)
        version = f"'{version}'"
        line = re.sub(r"'(.+?)'",version,line)
        
    with open('__init__.py','w') as file:
        file.write(line)

    version = re.findall(r"'(.+?)'",line)[-1]
    
    try:
        subprocess.call(['git', 'tag', f'v{version}'])
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
        
    