import os
import warnings
from dotenv import load_dotenv
from services.logger import Logger
from services.etl_services import ETLServiceHandler

# ignore warnings
warnings.filterwarnings("ignore")

# load environment variables
load_dotenv()

# create logger
logger = Logger()

# create etl service handler
etl = ETLServiceHandler()

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
    internal_ncs = etl.load_data(transaction_data_path,
                                 sheet_name=os.environ.get('INTERNAL_DATASOURCE'))
    external_ncs = etl.load_data(transaction_data_path,
                                 sheet_name=os.environ.get('EXTERNAL_DATASOURCE'))
    cost_product = etl.load_data(transaction_data_path,
                                 sheet_name=os.environ.get('COST_DATASOURCE'))
    
    # setting up transaction database
    logger.log("Setting up transaction database")
    etl.setup_db('transactions')

    # creating tables
    logger.log("Creating tables")
    etl.create_table(internal_ncs, 'internal_ncs')
    etl.create_table(external_ncs, 'external_ncs')
    etl.create_table(cost_product, 'cost_product')

    # end of ETL process
    logger.log("ETL process completed")
except Exception as e:
    logger.error(f"Error loading data from sources: {str(e)}")
    exit()

