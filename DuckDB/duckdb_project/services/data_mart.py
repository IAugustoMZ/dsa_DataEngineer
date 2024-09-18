import os
import json
import duckdb
import pandas as pd
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
    queries_primary_dimensions = {
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
        },
        "complaint_type_dimension":{
            "extract": """WITH raw_complaint_type AS (
                            SELECT DISTINCT tipo_reclamacao 
                            FROM transactions.main.external_ncs
                        )
                        SELECT ROW_NUMBER() OVER (ORDER BY tipo_reclamacao) AS complaint_type_id, 
                            tipo_reclamacao AS type_description  
                        FROM raw_complaint_type """,
            "load": """INSERT INTO complaint_type_dimension (complaint_type_id, complaint_type_name) VALUES (?, ?)"""
        },
        "issues_dimension":{
            "extract": """SELECT DISTINCT id_motivo, motivo, mao_de_obra, materia_prima,
                            maquina, meio_ambiente, 
                            medicao, metodo, recorrente 
                        FROM transactions.main.internal_ncs
                        ORDER BY id_motivo;""",
            "load": """INSERT INTO issues_dimension (issue_id, issue_name, is_labour, is_raw_material, is_machine, is_env, is_measure, is_method, is_recurrent) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        },
        "product_dimension":{
            "extract": """SELECT DISTINCT incs.id_produto, incs.produto_nome, encs.categoria, 
                                cost.custo_producao, incs.id_linha
                            FROM transactions.main.internal_ncs incs
                                JOIN transactions.main.external_ncs encs ON incs.id_produto = encs.id_produto
                                JOIN transactions.main.cost_product cost ON incs.id_produto = cost.id_produto
                            ORDER BY incs.id_produto""",
            "load": """INSERT INTO product_dimension (product_id, product_name, product_category, prod_line_fk, product_cost) VALUES (?, ?, ?, ?, ?)"""
        }
    }

    queries_secondary_dimensions = {
        "city_dimension":{
            "extract_1": """SELECT DISTINCT id_cidade, cidade, TRIM(estado) AS state
                            FROM transactions.main.external_ncs
                            ORDER BY id_cidade;""",
            "extract_2": """SELECT * 
                            FROM sink_data_mart.main.state_dimension;
                            """,
            "load": """INSERT INTO city_dimension (city_id, city_name, state_fk) VALUES (?, ?, ?)"""
        }
    }

    queries_facts = {
        "internal_ncs_fact":{
            "extract": """SELECT ROW_NUMBER () OVER (ORDER BY date) AS id,
                            date, id_produto AS prod_id_fk,
                            id_identificacaoNC AS process_step_fk,
                            id_motivo AS issues_fk, quantidadeNC AS qty_ncs 
                        FROM transactions.main.internal_ncs""",
            "load": """INSERT INTO internal_ncs_fact (internal_nc_id, date, prod_id_fk, process_step_fk, issues_fk, qty_ncs) VALUES (?, ?, ?, ?, ?, ?)"""
        },
        "external_ncs_fact":{
            "extract_1": """SELECT ROW_NUMBER() OVER (ORDER BY data) AS id,
                            "data" AS date_complaint, id_produto AS product_fk,
                            id_cidade AS city_fk, data_fabricacao AS fabrication_date,
                            id_motivo AS issue_fk, tipo_reclamacao AS type_fk,
                            quantidade AS qty_ncs
                        FROM transactions.main.external_ncs""",
            "extract_2": """SELECT * 
                            FROM sink_data_mart.main.complaint_type_dimension;""",
            "load": """INSERT INTO external_ncs_fact (external_nc_id, date_complaint, product_fk, city_fk, fabrication_date, issue_fk, type_fk, qty_ncs) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
        }
    }

    def __init__(self) -> None:
        """
        class to handle all data mart operations
        """
        super().__init__()
        # get the data mart path
        self.data_mart_path = os.path.join(ROOT_DIR, 'data', 'databases')

    def load_internal_ncs_fact(self) -> None:
        """
        loads data into the internal ncs fact table
        """
        # extract data
        query_extract = self.queries_facts['internal_ncs_fact']['extract']
        query_load = self.queries_facts['internal_ncs_fact']['load']

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
            logger.error(f"Error loading data into internal ncs fact: {e}")

    def load_external_ncs_fact(self) -> None:
        """
        loads data into the external ncs fact table
        """
        # extract data
        query_extract_1 = self.queries_facts['external_ncs_fact']['extract_1']
        query_extract_2 = self.queries_facts['external_ncs_fact']['extract_2']
        query_load = self.queries_facts['external_ncs_fact']['load']

        # establish connection to the source database
        conn_source = duckdb.connect(os.path.join(ROOT_DIR, 'data', 'databases', 'transactions.db'))
        conn_sink = duckdb.connect(os.path.join(ROOT_DIR, 'data', 'databases', 'sink_data_mart.db'))

        # extract data
        try:
            data_1 = pd.DataFrame(conn_source.execute(query_extract_1).fetchall(),
                                  columns=['id', 'date_complaint', 'product_fk', 'city_fk', 'fabrication_date', 'issue_fk', 'type_fk', 'qty_ncs'])
            data_2 = conn_sink.execute(query_extract_2).fetchall()

            # create a map of product names to product ids
            complaint_type_map = {complaint_type[1]: complaint_type[0] for complaint_type in data_2}

            # map the product names to the product ids
            data_1['type_fk'] = data_1['type_fk'].map(complaint_type_map)

            # transform the data frame into a list of tuples
            data_1 = [tuple(x) for x in data_1.to_numpy()]

            # load data
            conn_sink.executemany(query_load, data_1)
            conn_sink.commit()
        except Exception as e:
            logger.error(f"Error loading data into external ncs fact: {e}")

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
                cols += f"{col} {data_mart_schema['tables'][table][col]['type']}"
                
                # check if the column is the last column
                if col != list(data_mart_schema['tables'][table].keys())[-1]:
                    cols += ', '

            # format the query
            query = base_query.format(table_name=table, columns=cols)

            # execute the query
            self.conn.execute(query)
            self.conn.commit()

    def load_data_mart_primary_dimensions(self, table_name: str) -> None:
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
        query_extract = self.queries_primary_dimensions[table_name]['extract']
        query_load = self.queries_primary_dimensions[table_name]['load']

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

    def load_data_mart_secondary_dimensions_city(self) -> None:
        """
        loads data into the city dimension
        """

        # perform both extracts
        query_extract_1 = self.queries_secondary_dimensions['city_dimension']['extract_1']
        query_extract_2 = self.queries_secondary_dimensions['city_dimension']['extract_2']
        query_load = self.queries_secondary_dimensions['city_dimension']['load']

        # establish connection to the source database
        conn_source = duckdb.connect(os.path.join(ROOT_DIR, 'data', 'databases', 'transactions.db'))
        conn_sink = duckdb.connect(os.path.join(ROOT_DIR, 'data', 'databases', 'sink_data_mart.db'))

        # extract data
        try:
            data_1 = pd.DataFrame(conn_source.execute(query_extract_1).fetchall(),
                                  columns=['city_id', 'city_name', 'state_fk'])
            data_2 = conn_sink.execute(query_extract_2).fetchall()

            # create a map of state names to state ids
            state_map = {state[1]: state[0] for state in data_2}

            # map the state names to the state ids
            data_1['state_fk'] = data_1['state_fk'].map(state_map)

            # transform the data frame into a list of tuples
            data_1 = [tuple(x) for x in data_1.to_numpy()]

            # load data
            conn_sink.executemany(query_load, data_1)
            conn_sink.commit()
        except Exception as e:
            logger.error(f"Error loading data into city dimension: {e}")
            



    