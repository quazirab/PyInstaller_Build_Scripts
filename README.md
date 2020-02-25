Tested in python 3.6.6

### A typical top-level directory layout
    .
    ├── myModule
    │   ├── __init__.py (contains __version__ = '1.2.3.4' )
    ├── resources
    │   ├── productInfo.ini
    ├── build
    │   ├── debug.spec
    │   ├── release.spec
    ├── PyInstaller_build_Scripts
    │   ├── buildScript.py
    │   ├── msgPrepare.py
    │   ├── specCreator.py
    │   ├── versionInfoCreator.py
    │   ├── versionUpdate.py
    ├── ...

### buildScript.py
Builds the program to executable using `PyInstaller` and the `*.spec` file in build folder. Stores the debug executable in build\debug\version-x.x.x.x folder and release in build\release\version=x.x.x.x folder. 
Uses the `resoureces\productInfo.ini` to generate version information for MS Application Information.

Sample productInfo.ini
```
[Details]
Company = XYZ
ProductTitle = First App
ProductDescription = My First Windows Application
ProductName = First Application
Copyright = Personal No Copyright
```

To run the buildScript.py, from main directory run `python PyInstaller_Build_Scripts\buildScript`

## Git Hooks
### Commit Message Prepare
`msgPrepare.py` automatically adds version number from `__version__` in `__init__.py`. i.e. v1.1.0.1-My First commit

To activate the hook, copy the `prepare-commit-msg` file in .git>hooks.

### Version Update on Commit
`versionUpdate.py` automatically updates the file has part of the `__version__` in `__init__.py` with commit number. i.e __version__ = X.X.X.99

To activate the hook, copy the `pre-commit` fie in .git>hooks.