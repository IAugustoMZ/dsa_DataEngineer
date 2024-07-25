from datetime import datetime as dt

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
        print(f"{dt.now()} - [INFO] - {message}")

    def error(self, message: str):
        """
        Log an error message with timestamp

        Parameters
        ----------
        message : str
            The error message to be logged
        """
        print(f"{dt.now()} - [ERROR] - {message}")
