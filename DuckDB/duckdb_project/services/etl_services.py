import os
import duckdb
import pandas as pd

# get root folder
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class ETLServiceHandler:

    def __init__(self) -> None:
        """
        class to handle all ETL operations
        """
        # create databases folder if it does not exist
        if not os.path.isdir(os.path.join(ROOT_DIR, 'data', 'databases')):
            os.mkdir(os.path.join(ROOT_DIR, 'data', 'databases'))
    
    @staticmethod
    def load_data(data_path: str, sheet_name: str) -> pd.DataFrame:
        """
        Load data from a given path and sheet name
        """
        try:
            data = pd.read_excel(data_path, sheet_name=sheet_name)
            return data
        except:
            return None
        
    def setup_db(self, db_name: str) -> None:
        """
        Set up a database

        Parameters:
        ----------
        db_name: str
            name of the database to be created
        """
        # define the database path
        db_path = os.path.join(ROOT_DIR, 'data', 'databases', f'{db_name}.db')

        # create the database
        self.conn = duckdb.connect(db_path)

    def create_table(self, df: pd.DataFrame, table_name: str) -> None:
        """
        Create a table in the database

        Parameters:
        ----------
        df: pd.DataFrame
            dataframe to be saved as a table
        table_name: str
            name of the table to be created
        """
        # create the table
        df.to_sql(table_name, self.conn, index=False, if_exists='replace')
        

        