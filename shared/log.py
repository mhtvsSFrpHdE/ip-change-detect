import pathlib    # nopep8
import logging    # nopep8
from datetime import datetime    # nopep8

import config    # nopep8

def initLog(configLogType):
    logFolderName = config.logFolder
    logFolderName = logFolderName.replace(config.logTypePlaceholder, configLogType)
    logFolderPath = pathlib.Path(logFolderName)

    logFileName = config.logFileName
    logFileName = logFileName.replace(config.logTypePlaceholder, configLogType)
    logTimestamp = datetime.now().strftime(config.logTimestampFormat)
    logFileName = logFileName.replace(config.logTimestampPlaceholder, logTimestamp)

    logFilePath = logFolderPath.joinpath(logFileName)
    logFolderPath.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(filename=logFilePath, encoding='utf-8', format='%(asctime)s %(message)s', level=logging.NOTSET)

def printToLog(message, level=logging.INFO):
    logging.log(msg=message, level=level)
    print(message)
