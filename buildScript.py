import subprocess
import os
from configparser import ConfigParser
import re
from versionInfoCreator import versionDicCreator,versionTxtGenerator
from specCreator import specCreator

#### Version - {Major_Change,Minor_Change,Patch,Commit_Number}

buildLocation = 'build'

def build(versionNumber, buildType='debug'):
    '''
    Run the Build
    '''
    print(f'Building - {buildType}')
    os.chdir(buildLocation)
    if buildType=='debug':
        subprocess.call(f'pyinstaller --onefile --distpath ./debug/version-{versionNumber} rdebug.spec')
    else:
        subprocess.call(f'pyinstaller --onefile --nowindow --distpath ./release/version-{versionNumber} rrelease.spec')
    os.chdir('..')
    print(f'Finished building - {buildType}')

def versionUpdate(versionNumber, buildType='debug'):
    os.chdir(f'{buildLocation}')
    fileLocation = f'{buildType}/version-{versionNumber}'
    fileLocation = f'"{fileLocation}/{os.listdir(fileLocation)[-1]}"'
    subprocess.call(f'pyi-set_version file_version_info.txt {fileLocation}')
    os.chdir('..')

def versionFileDelete():
    os.chdir(f'{buildLocation}')
    if os.path.isfile('file_version_info.txt'):
        os.remove('file_version_info.txt')
    os.chdir('..')

def specFileDelete(buildType='debug'):
    os.chdir(f'{buildLocation}')
    if os.path.isfile(f'r{buildType}.spec'):
        os.remove(f'r{buildType}.spec')
    os.chdir('..')

def builder(versionNumber,buildType='debug'):
    '''
    Performs all the steps required for building the program
    1. Creates spec file
    2. Buids the program
    3. Deletes the spec file
    4. Updates the version information in the executable
    '''
    specCreator(buildType)
    # build(versionNumber, buildType)
    specFileDelete(buildType)
    # versionUpdate(versionNumber, buildType)

if __name__ == '__main__':
    # Generate Version Dictionary
    infoDic = versionDicCreator()
    # Generate file_version_info.txt using the generated Dictionary
    versionTxtGenerator(infoDic)
    
    # ------------------------------- Debug --------------------------------
    builder(infoDic['ProductVersion'])
    #-------------------------------- Release --------------------------------
    builder(infoDic['ProductVersion'],buildType='release')
    
    # Delete file_version_info.txt file
    versionFileDelete()
