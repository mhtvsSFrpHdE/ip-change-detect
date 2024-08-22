import pathlib    # nopep8
import logging    # nopep8
import os.path
from datetime import datetime    # nopep8
from time import sleep    # nopep8

import config    # nopep8

def initLog(configLogType):
    logFolderName = config.logFolder
    logFolderName = logFolderName.replace(config.logTypePlaceholder, configLogType)
    logFolderPath = pathlib.Path(logFolderName)
    logFolderPath.mkdir(parents=True, exist_ok=True)

    logFilePath = None

    # Prevent multiple instance log to same file
    fileNotAvailable = True
    while fileNotAvailable:
        # sleep: Make datetime.now() result more random in each loop
        sleep(0.1)
        logFileName = config.logFileName
        logFileName = logFileName.replace(config.logTypePlaceholder, configLogType)
        logTimestamp = datetime.now().strftime(config.logTimestampFormat)
        logFileName = logFileName.replace(config.logTimestampPlaceholder, logTimestamp)
        logFilePath = logFolderPath.joinpath(logFileName)
        try:
            # 'x': Create and open log file
            # Once file is opened, if other instance open same file will raise error
            with open(logFilePath, 'x'):
                fileNotAvailable = False
        except:
            # Error, wait for next log file name
            continue

    logging.basicConfig(filename=logFilePath, encoding='utf-8', format='%(asctime)s %(message)s', level=logging.NOTSET)

def printToLog(message, level=logging.INFO):
    logging.log(msg=message, level=level)
    print(message)
