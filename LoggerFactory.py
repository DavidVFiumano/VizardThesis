import logging
import csv
import os
import io
from typing import Optional, Union, Dict, List

import Configuration

# Written by GPT-4, very minimal clean up by David Fiumano

class CSVFormatter(logging.Formatter):
    def __init__(self, fieldnames: List[str], delimiter: str = ',', quotechar: str = '"', quoting: int = csv.QUOTE_MINIMAL, dialect : Union[str, csv.Dialect] = 'unix'):
        """
        Initialize the CSVFormatter with the specified fieldnames, delimiter, quote character, and quoting style.

        :param fieldnames: A list of fieldnames for the CSV log entry.
        :type fieldnames: List[str]
        :param delimiter: The character used to separate fields in the CSV log entry. Default is ','.
        :type delimiter: str
        :param quotechar: The character used to quote fields containing special characters. Default is '"'.
        :type quotechar: str
        :param quoting: The quoting style, as defined in the 'csv' module. Default is csv.QUOTE_MINIMAL.
        :type quoting: int
        """
        super().__init__()
        self.fieldnames = fieldnames
        self.delimiter = delimiter
        self.quotechar = quotechar
        self.quoting = quoting
        self.dialect = dialect
        self.wroteHeader = False

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the specified log record as a CSV log entry.

        :param record: The log record to be formatted.
        :type record: logging.LogRecord
        :return: The formatted CSV log entry.
        :rtype: str
        """
        log_entry = {fieldname: str(getattr(record, fieldname, '')) for fieldname in self.fieldnames}
        buffer = io.StringIO()            
        writer = csv.DictWriter(buffer, fieldnames=self.fieldnames, delimiter=self.delimiter,
                                quotechar=self.quotechar, quoting=self.quoting, dialect=self.dialect)
        if not self.wroteHeader:
            writer.writeheader()
            self.wroteHeader = True
        writer.writerow(log_entry)
        return buffer.getvalue().rstrip()

class LoggerSettingsError(Exception):
    pass
    
class LoggerNotInitializedError(Exception):
    pass

class LoggerFactory:
    loggers: Dict[str, logging.Logger] = {}
    parentDir: Union[str, None] = None

    @staticmethod
    def setParentDirectory(parentDirectory: str) -> None:
        """
        Set the parent directory for log files.

        :param parentDirectory: The parent directory path.
        :type parentDirectory: str
        """
        LoggerFactory.parentDir = parentDirectory

    @staticmethod
    def getLogger(name: str, level: int = logging.INFO, formatter: Optional[logging.Formatter] = None, file: Optional[str] = None) -> logging.Logger:
        """
        Get a logger with the specified name, level, formatter, and output file.
        
        If a logger with the specified name already exists and has different settings,
        a LoggerSettingsError will be raised.

        :param name: Name of the logger.
        :type name: str
        :param level: Logging level (e.g., logging.INFO, logging.DEBUG).
        :type level: int
        :param formatter: Logging message formatter.
        :type formatter: Optional[logging.Formatter]
        :param file: Output file name for logging.
        :type file: Optional[str]
        :return: Configured logger.
        :rtype: logging.Logger
        :raises LoggerSettingsError: If the logger with the specified name already exists with different settings.
        """
        if LoggerFactory.parentDir is None:
            raise LoggerNotInitializedError("LoggerFactory isn't initialized yet, wait until the global game state gets past ExperimentSetup to create/retrieve a logger!")
            
        if name in LoggerFactory.loggers:
            logger = LoggerFactory.loggers[name]
            existingLevel = logger.level
            existingFormatter = logger.handlers[0].formatter
            existingFile = logger.handlers[0].baseFilename if isinstance(logger.handlers[0], logging.FileHandler) else None

            if level != existingLevel or formatter != existingFormatter or file != os.path.basename(existingFile):
                raise LoggerSettingsError(f"Logger '{name}' already exists with different settings.")
            
            return logger

        logger = logging.getLogger(name)
        logger.setLevel(level)

        if formatter is None:
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        if file is not None:
            log_file_path = os.path.join(LoggerFactory.parentDir, file)
            os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
            fileHandler = logging.FileHandler(log_file_path)
            fileHandler.setFormatter(formatter)
            logger.addHandler(fileHandler)
        else:
            streamHandler = logging.StreamHandler()
            streamHandler.setFormatter(formatter)
            logger.addHandler(streamHandler)

        LoggerFactory.loggers[name] = logger

        return logger

# Example usage:
'''
# Set the parent directory for log files
LoggerFactory.setParentDirectory('my_game/logs')

# Get a logger that logs to console
gameLogger = LoggerFactory.getLogger('game')
gameLogger.info('Game started')

# Get a logger that logs to a file
errorLogger = LoggerFactory.getLogger('error', level=logging.ERROR, file='error')
errorLogger.error('An error occurred')

try:
    # Attempt to get a logger with the same name but different settings
    differentGameLogger = LoggerFactory.getLogger('game', level=logging.DEBUG, file='different_game')
except LoggerSettingsError as e:
    print(e)
'''