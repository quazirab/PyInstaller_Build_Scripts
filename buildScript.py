import subprocess
import os
from configparser import ConfigParser
import re
from fileVersionInfoCreator import versionDicCreator,versionTxtGenerator

#### Version - {Major_Change,Minor_Change,Patch,Commit_Number}

buildLocation = 'build'

def build_release(versionNumber):
    '''
    Run the Build for release
    '''
    print('Building release')
    os.chdir(buildLocation)
    subprocess.call(f'pyinstaller --onefile --distpath ./release/version-{versionNumber} release.spec')
    os.chdir('..')
    print('Finished building release')

def build_debug(versionNumber):
    '''
    Run the Build for debug
    '''
    print('Building debug')
    os.chdir(buildLocation)
    subprocess.call(f'pyinstaller --onefile --distpath ./debug/version-{versionNumber} debug.spec')
    os.chdir('..')

    print('Finished building debug')

def versionUpdate_debug(versionNumber):
    os.chdir(f'{buildLocation}')
    fileLocation = f'debug/version-{versionNumber}'
    fileLocation = f'"{fileLocation}/{os.listdir(fileLocation)[-1]}"'
    subprocess.call(f'pyi-set_version file_version_info.txt {fileLocation}')
    os.chdir('..')

def versionUpdate_release(versionNumber):
    os.chdir(f'{buildLocation}')
    fileLocation = f'release/version-{versionNumber}'
    fileLocation = f'"{fileLocation}/{os.listdir(fileLocation)[-1]}"'
    subprocess.call(f'pyi-set_version file_version_info.txt {fileLocation}')
    os.chdir('..')

def versionFileDelete():
    os.chdir(f'{buildLocation}')
    if os.path.isfile('file_version_info.txt'):
        os.remove('file_version_info.txt')

if __name__ == '__main__': 
    # Generate Version Dictionary
    infoDic = versionDicCreator()
    # Generate file_version_info.txt using the generated Dictionary
    versionTxtGenerator(infoDic)
    # Build Debug 
    build_debug(infoDic['ProductVersion'])
    # Update version Information of the executable file in debug
    versionUpdate_debug(infoDic['ProductVersion'])
    # Build Debug 
    build_release(infoDic['ProductVersion'])
    # Update version Information of the executable file in debug
    versionUpdate_release(infoDic['ProductVersion'])
    # Delete file_version_info.txt file
    versionFileDelete()
