import os
import duckdb
from src.model.filters.filter import Filter

# get the project root directory
ROOT_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__)
                )
            )
        )
    )
)

# get the path to the database
DATABASE_PATH = os.path.join(ROOT_DIR, 'data', 'databases','sink_data_mart.db')

class QualityDatabaseQueryHandler:

    def __init__(self):
        self.connection = duckdb.connect(DATABASE_PATH)

    def get_production_line(self) -> list:
        """
        gets all production lines

        Returns:
        --------
        list:
            list of production lines
        """
        query = 'SELECT DISTINCT production_line_name FROM production_line_dimension'
        return ['All'] + self.connection.execute(query).fetchdf()['production_line_name'].tolist()
    
    def get_products(self) -> list:
        """
        gets all products

        Returns:
        --------
        list:
            list of products
        """
        query = 'SELECT DISTINCT product_name FROM product_dimension'
        return ['All'] + self.connection.execute(query).fetchdf()['product_name'].tolist()
    
    def get_total_internal_ncs(self, filter: Filter) -> int:
        """
        gets the total number of internal non-conformities

        Args:
        -----
        filter (Filter):
            filter object

        Returns:
        --------
        int:
            total number of internal non-conformities
        """
        base_query = f"""
        SELECT SUM(f.qty_ncs) AS total_internal_ncs
        FROM internal_ncs_fact f
            INNER JOIN product_dimension prd
                ON f.prod_id_fk = prd.product_id 
            INNER JOIN production_line_dimension pl
                ON prd.prod_line_fk = pl.production_line_id
        WHERE f.date BETWEEN '{filter.start_date}' AND '{filter.end_date}'
        """
        if filter.production_line != 'All':
            base_query += f' AND production_line_name = "{filter.production_line}"'
        if filter.product != 'All':
            base_query += f' AND product_name = "{filter.product}"'
        
        data = self.connection.execute(base_query).fetchdf().iloc[0, 0]
        if str(data).lower() == 'nan':
            return '-'
        else:
            return int(data)