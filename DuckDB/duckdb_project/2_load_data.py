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
logger.log("Starting to load the data mart - Primary Dimensions")

for table in data_mart.queries_primary_dimensions:
    data_mart.load_data_mart_primary_dimensions(table)

# load the secondary dimensions
logger.log("Starting to load the data mart - Secondary Dimensions - City")
data_mart.load_data_mart_secondary_dimensions_city()

# load the fact tables
logger.log("Starting to load the data mart - Fact Tables - Internal Non-Conformities")
data_mart.load_internal_ncs_fact()

logger.log("Starting to load the data mart - Fact Tables - External Non-Conformities")
data_mart.load_external_ncs_fact()