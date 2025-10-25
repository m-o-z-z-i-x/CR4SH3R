# ---------------------------------------------------------------------------- #
# DESCRIPTION: custom logger for execution reports with file and line context
# ---------------------------------------------------------------------------- #

# DEPENDENCIES --------------------------------------------------------------- #
from os import path, makedirs
from logging import basicConfig, INFO, getLogger
from traceback import extract_tb
# ---------------------------------------------------------------------------- #

# LOGIC ---------------------------------------------------------------------- #
logFilePath = "./logs/execution-report.log"

# create directory if it doesn't exist
logDir = path.dirname(logFilePath)

if not path.exists(logDir):
  makedirs(logDir)

# create empty log file if it doesn't exist
if not path.exists(logFilePath):
  with open(logFilePath, "w"):
    pass # just create an empty file

# configure logging
basicConfig(
  level = INFO,
  format = "[%(asctime)s] -- %(message)s",
  datefmt = "%Y-%m-%d %H:%M:%S",
  filename = logFilePath
)

logger = getLogger(__name__)

def message(text, type = "info"):
  logger.info(text)

def exception(message):
  # extract traceback info for error logging
  tb = extract_tb(message.__traceback__)
  filename, line, func, text = tb[-1]
  filename = path.basename(filename)

  # log error with file and line context
  logger.error(f"[FILE] {filename} -- [LINE] {line}: {str(message)}")
# ---------------------------------------------------------------------------- #