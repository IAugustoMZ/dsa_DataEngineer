import os
from dotenv import load_dotenv

# get environment variables
env_path = os.path.join(
    os.path.dirname(
        os.path.dirname(
            os.path.realpath(__file__)
        )
    ), '.env'
)

# load environment variables
load_dotenv(dotenv_path=env_path)

class DuckDBConnectionHandler:
    def __init__(self):
        """
        DuckDB database connection handler
        """
        self.connection = None

    def connect(self, database=None):
        if not database:
            database = os.environ.get('DUCKDB_DATABASE')
        self.connection = duckdb.connect(database=database)
        return self.connection

    def execute(self, query):
        return self.connection.execute(query)

    def close(self):
        self.connection.close()

    def __del__(self):
        self.close()