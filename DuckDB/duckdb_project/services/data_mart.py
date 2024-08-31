import os
import json
from .etl_services import ETLServiceHandler

# get root directory
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# load json with the data mart schema
with open(os.path.join(ROOT_DIR, 'data_models', 'data_mart_schema.json'), 'r') as f:
    data_mart_schema = json.load(f)

class DataMartServiceHandler(ETLServiceHandler):
    def __init__(self) -> None:
        """
        class to handle all data mart operations
        """
        super().__init__()

    