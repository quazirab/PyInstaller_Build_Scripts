## Features
1. Auto increment x in `__version__ = '0.0.0.x'` in `__init__` file
1. Tag and modify commit message with the version number
1. Build executables as per the `*.spec` files
1. Assign MS Application Information to the executables 

## Limitation
The repo name must be same as the module name. 

## A typical top-level directory layout
    .
    ├── myModule
    │   ├── __init__.py (contains __version__ = '1.2.3.4' )
    ├── resources
    │   ├── productInfo.toml
    │   ├── icon.ico
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

## Installation

1. Use `git submodule add <git url>` to clone the module in your repo. 
1. Copy the build and resourses folder in the `PyInstaller_build_Scripts/examples` to main directory and modify it as per your need

## Build
Build the program to executable using `PyInstaller` and the `*.spec` file in build folder. It will store the debug executable in `build\debug\version-x.x.x.x` folder and release in `build\release\version=x.x.x.x folder`. 
Uses the `resoureces\productInfo.toml` to generate version information for MS Application Information.

Sample productInfo.toml
```
[Details]
Company = "XYZ"
ProductTitle = "First App
ProductDescription = "My First Windows Application"
ProductName = "First Application"
Copyright = "Personal No Copyright"
```

To run the `buildScript.py`, from main directory run `python PyInstaller_Build_Scripts\buildScript.py`

## Git Hooks

### Version Update on Commit
`versionUpdate.py` automatically updates the file has part of the `__version__` in `__init__.py` with commit number. i.e __version__ = X.X.X.99

To activate the hook, copy the `pre-commit` fie in .git>hooks.

### Commit Message Prepare
`msgPrepare.py` automatically adds version number from `__version__` in `__init__.py`. i.e. v1.1.0.1-My First commit

To activate the hook, copy the `prepare-commit-msg` file in .git>hooks.


### Requirements

1. Tested in python 3.6.6
2. `pip install toml`


Feel free to clone it and if you have any suggestion or advice, give me a shout : quazi.rabbi@gmail.com