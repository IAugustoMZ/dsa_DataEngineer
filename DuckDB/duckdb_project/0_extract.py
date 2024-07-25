import os
import duckdb
import pandas as pd
from dotenv import load_dotenv
from services.logger import Logger

# load environment variables
load_dotenv()

# create logger
logger = Logger()

# get datasources and transaction data path
logger.log("Getting data sources and transaction data path")
transaction_data_path = os.environ.get('OLTP_TOOL_PATH')
quality_transactions = os.environ.get('OLAP_TOOL_PATH')

if not transaction_data_path or not quality_transactions:
    logger.error("Datasources or transaction data path not found")
    exit()

# load all dataframes
logger.log("Loading data from sources")
try:
    internal_ncs = pd.read_excel(transaction_data_path,
                                sheet_name=os.environ.get('INTERNAL_DATASOURCE'))
    external_ncs = pd.read_excel(transaction_data_path,
                                sheet_name=os.environ.get('EXTERNAL_DATASOURCE'))
    cost_product = pd.read_excel(transaction_data_path,
                                sheet_name=os.environ.get('COST_DATASOURCE'))
except Exception as e:
    logger.error(f"Error loading data from sources: {str(e)}")
    exit()

