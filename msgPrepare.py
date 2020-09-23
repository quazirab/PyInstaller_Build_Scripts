'''
Authur : Quazi Rabbi
Objective : read current version number from __init__.py and add it to the git message
How it works :  1. read the git message from .git/COMMIT_EDITMSG
                2. read the __version__ in __init__.py
                3. combine the msg with version at the front, msg cut if more than 72 characters.

Additional Step - to run as git pre-commit hook - add a file 'pre-commit' (no file extension) in .git->hooks with the following lines :
                #!/bin/sh
                # To enable this hook, rename this file to "pre-commit".

                python3 PyInstaller_Build_Scripts\\msgPrepare.py
'''
import sys,os,re,subprocess

def getVersion(moduleName=None):
    '''
    Returns the version string from the __init__.py
    '''
    if not moduleName:
        moduleName = os.getcwd().split('\\')[-1]
    sys.path.append('.')

    init_file_path = os.path.join(moduleName,'__init__.py')

    with open(init_file_path,'r') as handler:
        for cnt, line in enumerate(handler):
            if '__version__' and  "=" in line:
                version = line[line.find('=')+1:].strip()
                if "'" or '"' in version:
                    return version

def updateCommitMessage(version):
    os.chdir('./.git')
    line = None
    with open('COMMIT_EDITMSG','r') as file:
        line = file.read()
    line = f'v{version}-{line}'

    line=(line[:70]+'..') if len(line)>72 else line

    with open('COMMIT_EDITMSG','w') as file:
        file.write(line) 

if __name__ == "__main__":
    # print(getVersion())
    updateCommitMessage(getVersion())