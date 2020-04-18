#!/usr/bin/python
# -*- coding:utf -8 -*-

import os
import subprocess
from benderPDF import __version__

### Настройки сборки приложения: ###
# имя приложения:
APP_NAME = 'BenderPDF'
# версия приложения
APP_VERSION = __version__
# иконка приложения
APP_ICON = '\\bender.ico'
# тип системы
SYSTEM_NAME = os.name
# расположение Pyinstaller'а
ABSOLUTE_PATH = os.path.abspath('')
PATH = '\\venv\\Scripts\\'
PYINSTALLER_NAME = 'pyinstaller.exe'
COMMAND = ABSOLUTE_PATH + PATH + PYINSTALLER_NAME
## Для использования своего .spec файла ##
SPEC = 'benderPDF.spec'
## Опции: ##
# Clean PyInstaller cache and remove temporary files before building.
CLEAN = '--clean'
# Replace output directory (default: SPECPATH/dist/SPECNAME) without asking for confirmation
NONECONFIRM = '--noconfirm'
# Create a one-folder bundle containing an executable (default)
ONEDIR = '--onedir'
# Create a one-file bundled executable.
ONEFILE = '--onefile'
# Name to assign to the bundled app and spec file (default: first script’s basename)
NAME = '--name '
SCRIPT_NAME = APP_NAME + '.py'
# Windows and Mac OS X: do not provide a console window for standard i/o.
# On Mac OS X this also triggers building an OS X .app bundle.
# This option is ignored in *NIX systems.
NOCONSOLE = '--noconsole'
# Open a console window for standard i/o (default)
NOWINDOWED = '--nowindowed'
# FILE.ico: apply that icon to a Windows executable.
ICON = '--icon ' + ABSOLUTE_PATH + APP_ICON
# add a version resource from FILE to the exe
VERSION_FILE = ''
VERSION = "--version-file " + VERSION_FILE
# A path to search for imports (like using PYTHONPATH).
# Multiple paths are allowed, separated by ‘:’, or use this option multiple times
PATHS = '--paths ' + ABSOLUTE_PATH
# Do not use UPX even if it is available (works differently between Windows and *nix)
NOUPX = '--noupx'

subprocess.call([COMMAND, NOUPX, CLEAN, ONEFILE,
                 NOCONSOLE, SCRIPT_NAME])
