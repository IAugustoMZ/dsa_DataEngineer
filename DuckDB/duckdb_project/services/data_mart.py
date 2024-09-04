import os
import json
import duckdb
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

    # map of queries to extract from transaction data and load into the data mart
    queries = {
        "production_line_dimension": {
            "extract": """SELECT DISTINCT id_linha, linha
                        FROM internal_ncs
                        ORDER BY id_linha """,
            "load": """INSERT INTO production_line_dimension (production_line_id, production_line_name) VALUES (?, ?)"""
        },
        "process_steps_dimension": {
            "extract": """SELECT DISTINCT id_identificacaoNC, local_identificacao
                        FROM transactions.main.internal_ncs
                        ORDER BY id_identificacaoNC""",
            "load": """INSERT INTO process_steps_dimension (process_step_id, process_step_name) VALUES (?, ?)"""
        },
        "state_dimension": {
            "extract": """WITH raw_state AS (
                            SELECT DISTINCT estado,
                            FROM transactions.main.external_ncs
                        )
                        SELECT ROW_NUMBER() OVER (ORDER BY estado) AS state_id,
                            CASE 
                                WHEN state_id = 1 THEN 'Bahia'
                                WHEN state_id = 2 THEN 'Pará'
                                ELSE TRIM(estado) 
                            END AS state_name,
                            CASE
                                WHEN state_id = 1 THEN 'BA'
                                WHEN state_id = 2 THEN 'PA'
                                WHEN state_id = 3 THEN 'AC'
                                WHEN state_id = 4 THEN 'AL'
                                WHEN state_id = 5 THEN 'AP'
                                WHEN state_id = 6 THEN 'AM'
                                WHEN state_id = 7 THEN 'CE'
                                WHEN state_id = 8 THEN 'DF'
                                WHEN state_id = 9 THEN 'ES'
                                WHEN state_id = 10 THEN 'GO'
                                WHEN state_id = 11 THEN 'MA'
                                WHEN state_id = 12 THEN 'MT'
                                WHEN state_id = 13 THEN 'MS'
                                WHEN state_id = 14 THEN 'MG'
                                WHEN state_id = 15 THEN 'PR'
                                WHEN state_id = 16 THEN 'PB'
                                WHEN state_id = 17 THEN 'PE'
                                WHEN state_id = 18 THEN 'PI'
                                WHEN state_id = 19 THEN 'RN'
                                WHEN state_id = 20 THEN 'RS'
                                WHEN state_id = 21 THEN 'RJ'
                                WHEN state_id = 22 THEN 'RO'
                                WHEN state_id = 23 THEN 'RR'
                                WHEN state_id = 24 THEN 'SC'
                                WHEN state_id = 25 THEN 'SE'
                                WHEN state_id = 26 THEN 'SP'
                                ELSE 'TO'
                            END AS state_code
                        FROM raw_state""",
            "load": """INSERT INTO state_dimension (state_id, state_name, state_code) VALUES (?, ?, ?)"""
        }
    }

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

    def load_data_mart(self, table_name: str) -> None:
        """
        load data into the data mart

        Parameters
        ----------
        table_name : str
            name of the table to load data into
        """
        # log the table being loaded
        logger.log(f"Loading data into {table_name}")

        # get the queries
        query_extract = self.queries[table_name]['extract']
        query_load = self.queries[table_name]['load']

        # establish connection to the source database
        conn_source = duckdb.connect(os.path.join(ROOT_DIR, 'data', 'databases', 'transactions.db'))
        conn_sink = duckdb.connect(os.path.join(ROOT_DIR, 'data', 'databases', 'sink_data_mart.db'))

        # extract data
        try:
            data = conn_source.execute(query_extract).fetchall()

            # load data
            conn_sink.executemany(query_load, data)
            conn_sink.commit()
        except Exception as e:
            logger.error(f"Error loading data into {table_name}: {e}")

            

            



    