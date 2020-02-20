'''
Authur : Quazi Rabbi
Objective : generate file_version_info.txt for pyinstaller builds, the generated file will be installed in build folder in main directory
How it works :  1. find the module name, which must should be same as main directory name .../documents/myModule/myModule/__init__.py
                    if the module name is not same as main directory name - then run python fileVersionInfoCreator.py myModule
                2. reads the productInfo.ini in resources folder in main directory, i.e. :
                # main directory/resources/productInfo.ini
                [Details]
                Company = ABC
                ProductTitle = XYZ
                ProductDescription = Hello Application
                ProductName = XYZ
                Copyright = Free for all 2020
                3. Outputs a file_version_info.txt file ,main directory/build folder
'''
import os,sys
from configparser import ConfigParser
from datetime import datetime

def versionTxtGenerator(infoDic):
    info =f'''VSVersionInfo(
        ffi=FixedFileInfo(
            # filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
            # Set not needed items to zero 0.
            filevers={infoDic.get('filevers','(1, 0, 1, 9)')},
            prodvers={infoDic.get('prodvers','(1, 0, 0, 1)')},
            # Contains a bitmask that specifies the valid bits 'flags'r
            mask={infoDic.get('mask','0x3f')},
            # Contains a bitmask that specifies the Boolean attributes of the file.
            flags={infoDic.get('flags','0x8')},
            # The operating system for which this file was designed.
            # 0x4 - NT and there is no need to change it.
            OS={infoDic.get('OS','0x40004')},
            # The general type of file.
            # 0x1 - the file is an application.
            fileType={infoDic.get('fileType','0x1')},
            # The function of the file.
            # 0x0 - the function is not defined for this fileType
            subtype={infoDic.get('subtype','0x0')},
            # Creation date and time stamp.
            date={infoDic.get('date','(0, 0)')}
            ),
        kids=[
            StringFileInfo(
            [
            StringTable(
                u'000004b0',
                [StringStruct(u'FileVersion', u'{infoDic.get('FileVersion','1.0.1.9')} [{infoDic.get('Date','26-Jul-2011')}]'),
                StringStruct(u'ProductVersion', u'{infoDic.get('ProductVersion','1.0.0.1')}'),
                StringStruct(u'OriginalFilename', u'{infoDic.get('OriginalFilename','')}'),
                StringStruct(u'InternalName', u'{infoDic.get('InternalName','verpatch.exe')}'),
                StringStruct(u'FileDescription', u'{infoDic.get('FileDescription','verpatch.exe')}'),
                StringStruct(u'CompanyName', u'{infoDic.get('FileDescription','Version patcher too')}'),
                StringStruct(u'LegalCopyright', u'{infoDic.get('LegalCopyright','(C) 1998-2011, pavel_a')}'),
                StringStruct(u'ProductName', u'{infoDic.get('ProductName','')}'),
                StringStruct(u'PrivateBuild', u'{infoDic.get('PrivateBuild','pa')}')])
            ]), 
            VarFileInfo([VarStruct(u'Translation', [0, 1200])])
        ]
        )'''

    with open('build\\file_version_info.txt','w') as file:
        file.write(info)

def versionDicCreator(moduleName=None):
    if not moduleName:
        moduleName = os.getcwd().split('\\')[-1]
    import sys
    sys.path.append('.')
    ver = __import__(f'{moduleName}').__version__

    productInfo = ConfigParser()
    productInfo.optionxform = str
    productInfo.read('resources\\productInfo.ini')


    filevers = ver.split('.')
    filevers = ', '.join(filevers)
    
    date = datetime.now().strftime("%d-%b-%Y")


    infoDic = {
        'filevers': f'({filevers})',
        'prodvers':f'({filevers})',
        'FileVersion':ver,
        'ProductVersion':ver,
        'OriginalFilename':productInfo['Details']['ProductTitle'],
        'InternalName':productInfo['Details']['ProductName'],
        'FileDescription':productInfo['Details']['ProductDescription'],
        'CompanyName':productInfo['Details']['Company'],
        'LegalCopyright':productInfo['Details']['Copyright'],
        'ProductName':productInfo['Details']['ProductName'],
        'Date':date

    }
    return infoDic

if __name__ == "__main__":
    # a = {}
    # versionTxtGenerator(a)
    moduleName = sys.argv[-1]
    infoDic = None
    if '.py' in moduleName:
        infoDic = versionDicCreator()
    else:
        infoDic = versionDicCreator(moduleName)
    versionTxtGenerator(infoDic)
