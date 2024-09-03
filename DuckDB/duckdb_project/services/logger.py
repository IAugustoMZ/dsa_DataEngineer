import os
from datetime import datetime as dt

# get root folder
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# log file path
LOG_FILE = os.path.join(ROOT_DIR, 'logs')

class Logger:
    def __init__(self):
        """
        Initialize the logger class
        """
        pass

    def log(self, message: str):
        """
        Log a message with timestamp

        Parameters
        ----------
        message : str
            The message to be logged
        """
        # the name is the current date without dashes
        name = str(dt.now().date()).replace('-', '').replace(' ', '').replace(':', '')

        # create the log file
        with open(os.path.join(LOG_FILE, f'{name}.log'), 'a') as f:
            f.write(f"{dt.now()} - [INFO] - {message}\n")

        print(f"{dt.now()} - [INFO] - {message}")

    def error(self, message: str):
        """
        Log an error message with timestamp

        Parameters
        ----------
        message : str
            The error message to be logged
        """
        # the name is the current date without dashes
        name = str(dt.now().date()).replace('-', '').replace(' ', '').replace(':', '')

        # create the log file
        with open(os.path.join(LOG_FILE, f'{name}.log'), 'a') as f:
            f.write(f"{dt.now()} - [ERROR] - {message}\n")

        print(f"{dt.now()} - [ERROR] - {message}")
