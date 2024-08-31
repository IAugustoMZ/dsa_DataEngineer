import os
import warnings
from dotenv import load_dotenv
from services.logger import Logger
from services.etl_services import ETLServiceHandler
from services.data_mart import DataMartServiceHandler

# ignore warnings
warnings.filterwarnings("ignore")

# load environment variables
load_dotenv()

# create logger
logger = Logger()

# create etl service handler
etl = ETLServiceHandler()

# create data mart service handler
data_mart = DataMartServiceHandler()

# get datasources and transaction data path
logger.log("Getting data sources and transaction data path")
transaction_data_path = os.environ.get('OLTP_TOOL_PATH')
quality_transactions = os.environ.get('OLAP_TOOL_PATH')

# create the sink database
logger.log("Creating the sink database")
data_mart.setup_db('sink_olap')

# creating the sinf data mart schemas
data_mart.create_sink_data_mart()