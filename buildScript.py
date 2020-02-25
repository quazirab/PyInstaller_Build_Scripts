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
    subprocess.call(f'pyi-set_version file_version_info_{buildType}.txt {fileLocation}')
    os.chdir('..')

def versionFileDelete(buildType='debug'):
    os.chdir(f'{buildLocation}')
    if os.path.isfile(f'file_version_info_{buildType}.txt'):
        os.remove(f'file_version_info_{buildType}.txt')
    os.chdir('..')

def specFileDelete(buildType='debug'):
    os.chdir(f'{buildLocation}')
    if os.path.isfile(f'r{buildType}.spec'):
        os.remove(f'r{buildType}.spec')
    os.chdir('..')

def builder(buildType='debug'):
    '''
    Performs all the steps required for building the program
    1. Creates the version information dictionary
    2. Creates spec file for build
    3. Builds the program
    4. Deletes the spec file
    5. Generates version file information for MS Application executable
    6. Updates the version information in the executable
    7. Deletes the version file
    '''
    infoDic = versionDicCreator(buildType)
    specCreator(buildType)
    build(infoDic['ProductVersion'], buildType)
    specFileDelete(buildType)
    versionTxtGenerator(infoDic,buildType)
    versionUpdate(infoDic['ProductVersion'], buildType)
    versionFileDelete(buildType)

if __name__ == '__main__':

    # ------------------------------- Debug --------------------------------
    builder()
    #-------------------------------- Release --------------------------------
    builder(buildType='release')
    
