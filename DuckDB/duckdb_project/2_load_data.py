import warnings
from dotenv import load_dotenv
from services.logger import Logger
from services.data_mart import DataMartServiceHandler

# ignore warnings
warnings.filterwarnings("ignore")

# load environment variables
load_dotenv()

# create logger
logger = Logger()

# create data mart service handler
data_mart = DataMartServiceHandler()

# start loading the data mart
logger.log("Starting to load the data mart")

for table in data_mart.queries:
    data_mart.load_data_mart(table)