import os
import json
from services.logger import Logger
from .etl_services import ETLServiceHandler

# get root directory
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# create logger
logger = Logger()

# load json with the data mart schema
with open(os.path.join(ROOT_DIR, 'data_models', 'data_mart_schema.json'), 'r') as f:
    data_mart_schema = json.load(f)

class DataMartServiceHandler(ETLServiceHandler):
    def __init__(self) -> None:
        """
        class to handle all data mart operations
        """
        super().__init__()
        # get the data mart path
        self.data_mart_path = os.path.join(ROOT_DIR, 'data', 'databases')

    def create_sink_data_mart(self, data_mart_name: str) -> None:
        """
        create a data mart

        Parameters
        ----------
        data_mart_name : str
            name of the data mart to create
        """
        # establish DuckDB connection
        self.setup_db(data_mart_name)

        # base query
        base_query = """CREATE TABLE IF NOT EXISTS {table_name} ({columns})"""

        # create the data mart schema
        for table in data_mart_schema['tables']:
            # log the table being created
            logger.log(f"Creating table {table}")
            cols = ''
            for col in data_mart_schema['tables'][table]:
                if col != 'foreign_key':
                    cols += f"{col} {data_mart_schema['tables'][table][col]['type']}"

                    # check if the column is a primary key
                    if 'primary_key' in data_mart_schema['tables'][table][col]:
                        cols += ' PRIMARY KEY'
                    
                    # check if the column is the last column
                    if col != list(data_mart_schema['tables'][table].keys())[-1]:
                        cols += ', '

            # check if the table has a foreign key
            if 'foreign_key' in data_mart_schema['tables'][table]:
                
                for fk in data_mart_schema['tables'][table]['foreign_key']:
                    # check if the fk is the first fk
                    if fk == list(data_mart_schema['tables'][table]['foreign_key'].keys())[0]:
                        cols += f"FOREIGN KEY ({fk}) REFERENCES {data_mart_schema['tables'][table]['foreign_key'][fk]['table']}({data_mart_schema['tables'][table]['foreign_key'][fk]['column']})"
                    else:
                        cols += f", FOREIGN KEY ({fk}) REFERENCES {data_mart_schema['tables'][table]['foreign_key'][fk]['table']}({data_mart_schema['tables'][table]['foreign_key'][fk]['column']})"

            # format the query
            query = base_query.format(table_name=table, columns=cols)

            # execute the query
            self.conn.execute(query)
            self.conn.commit()

            

            



    