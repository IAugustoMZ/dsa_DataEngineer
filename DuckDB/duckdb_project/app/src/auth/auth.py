import os
from dotenv import load_dotenv

# get dot env file
dotenv_path = os.path.join(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__)
                )
            )
        )
    ),
    '.env'
)
load_dotenv(dotenv_path)

class AuthHandler:
    def __init__(self):
        """
        simple authentication handler
        """
        pass

    def login(self, username: str, password: str) -> bool:
        """
        login method

        Parameters:
        ----------
        username: str
            username
        password: str
            password

        Returns:
        --------
        bool
            True if login is successful, False
        """
        if username == os.environ.get('APP_USER') and password == os.environ.get('APP_PASSWORD'):
            return True
        return False