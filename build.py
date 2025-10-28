# -*- coding: utf-8 -*-

# DEPENDENCIES --------------------------------------------------------------- #
import os
import shutil
from subprocess import run

# external
from dotenv import load_dotenv
# ---------------------------------------------------------------------------- #

# LOGIC ---------------------------------------------------------------------- #
load_dotenv()

author = os.getenv("AUTHOR")
appName = os.getenv("APP_NAME")
appVersion = os.getenv("APP_VERSION")
description = os.getenv("DESCRIPTION")
command = [
  ".venv\\Scripts\\nuitka.cmd",

  # compilation options
  "--standalone", # create self-contained distribution
  "--onefile", # create single executable
  "--windows-console-mode=disable", # disable console for pyqt5 app

  # compiler options
  "--mingw64", # use mingw64 compiler
  "--enable-plugin=pyqt5", # enable pyqt5 plugin (critical for pyqt5 apps)

  # output configuration
  f"--output-dir=dist", # build directory
  f"--output-filename={appName}", # final executable name

  # windows metadata
  f"--windows-icon-from-ico=res/icons/logo.png", # application icon
  f"--product-name={appName}", # product name
  f"--file-version={appVersion}", # file version
  f"--product-version={appVersion}", # product version
  f"--copyright={author}", # copyright info
  f"--file-description={description}", # file description

  # dependency control
	f"--include-data-file={os.path.abspath('.env')}=.env", # include encrypted file
  "--include-package=urllib3", # follow all urllib3 imports recursively

  # optimization
  "--enable-plugin=upx", # enable upx compression
  f"--upx-binary={os.path.abspath('tools/upx')}", # custom upx path

  # debugging and reporting
  "--show-progress", # show compilation progress
  "--show-modules", # display included modules
  "--report=logs/compilation-report.xml", # generate build report

  "main.py"
]

run(command, shell=True)

# distribution structure
distPath = os.path.join("dist")

# create res directory in dist
resPath = os.path.join(distPath, "res")

if not os.path.exists(resPath):
  os.makedirs(resPath)

# copy resources
resources = [
  "./res/vpaths",
  "./res/result.xlsx",
]

for item in resources:
  src = os.path.normpath(item)
  dst = os.path.join(resPath, os.path.basename(src))

  if os.path.isdir(src):
    shutil.copytree(src, dst)
  elif os.path.isfile(src):
    shutil.copy2(src, dst)
# ---------------------------------------------------------------------------- #