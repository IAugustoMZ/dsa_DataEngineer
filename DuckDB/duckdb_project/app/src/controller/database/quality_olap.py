import os
import duckdb
import pandas as pd
from src.model.filters.filter import Filter

# get the path to the database
DATABASE_PATH = os.path.join('data', 'databases', 'sink_data_mart.db')

class QualityDatabaseQueryHandler:

    def __init__(self):
        duckdb.close()
        self.connection = duckdb.connect(DATABASE_PATH, read_only=True)

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
            base_query += f" AND production_line_name = '{filter.production_line}'"
        
        data = self.connection.execute(base_query).fetchdf().iloc[0, 0]
        if str(data).lower() == 'nan':
            return '-'
        else:
            return int(data)

    def get_total_defects_cost(self, filter: Filter) -> int:
        """
        gets the total cost of defects

        Args:
        -----
        filter (Filter):
            filter object

        Returns:
        --------
        int:
            total cost of defects
        """
        base_query = f"""
        SELECT SUM(f.qty_ncs * p.product_cost) AS nc_cost
        FROM sink_data_mart.main.internal_ncs_fact f
            INNER JOIN sink_data_mart.main.product_dimension p
                ON f.prod_id_fk = p.product_id
            INNER JOIN sink_data_mart.main.production_line_dimension pl
                ON p.prod_line_fk = pl.production_line_id
        WHERE f.date BETWEEN '{filter.start_date}' AND '{filter.end_date}'
        """
        if filter.production_line != 'All':
            base_query += f" AND pl.production_line_name = '{filter.production_line}'"
        
        data = self.connection.execute(base_query).fetchdf().iloc[0, 0]
        if str(data).lower() == 'nan':
            return '-'
        else:
            return int(data)

    def get_evolution_defects(self, filter: Filter) -> pd.DataFrame:
        """
        gets the evolution of defects

        Args:
        -----
        filter (Filter):
            filter object

        Returns:
        --------
        pd.DataFrame:
            pd.DataFrame of defects evolution
        """
        if filter.start_date[:7] != filter.end_date[:7]:
            base_query = f"""
            SELECT CONCAT(MONTH(f.date), ' - ', YEAR(f.date)) as date, SUM(f.qty_ncs) AS total_ncs
            FROM sink_data_mart.main.internal_ncs_fact f
                INNER JOIN sink_data_mart.main.product_dimension p
                    ON f.prod_id_fk = p.product_id
                INNER JOIN sink_data_mart.main.production_line_dimension pl
                    ON p.prod_line_fk = pl.production_line_id
            WHERE f.date BETWEEN '{filter.start_date}' AND '{filter.end_date}'
            """
            if filter.production_line != 'All':
                base_query += f" AND pl.production_line_name = '{filter.production_line}'"
            
            base_query += " GROUP BY CONCAT(MONTH(f.date), ' - ', YEAR(f.date))"
            base_query += ' ORDER BY date'
        else:
            base_query = f"""
            SELECT f.date as date, SUM(f.qty_ncs) AS total_ncs
            FROM sink_data_mart.main.internal_ncs_fact f
                INNER JOIN sink_data_mart.main.product_dimension p
                    ON f.prod_id_fk = p.product_id
                INNER JOIN sink_data_mart.main.production_line_dimension pl
                    ON p.prod_line_fk = pl.production_line_id
            WHERE f.date BETWEEN '{filter.start_date}' AND '{filter.end_date}'
            """
            if filter.production_line != 'All':
                base_query += f" AND pl.production_line_name = '{filter.production_line}'"
        
            base_query += ' GROUP BY f.date'
            base_query += ' ORDER BY date'

        data = self.connection.execute(base_query).fetchdf()

        # date come as string, we need to convert it to datetime
        data['date'] = pd.to_datetime(data['date'])

        return data
    
    def get_most_defective_product(self, filter: Filter, top_k: int = 5) -> pd.DataFrame:
        """
        query to get the most defective product

        Args:
        -----
        filter (Filter):
            filter object
        top_k (int):
            top k products to return

        Returns:
        --------
        pd.DataFrame:
            pd.DataFrame of the most defective products
        """
        base_query = f"""
        SELECT p.product_name, SUM(f.qty_ncs) AS total_ncs
        FROM sink_data_mart.main.internal_ncs_fact f
            INNER JOIN sink_data_mart.main.product_dimension p
                ON f.prod_id_fk = p.product_id
            INNER JOIN sink_data_mart.main.production_line_dimension pl
                ON p.prod_line_fk = pl.production_line_id
        WHERE f.date BETWEEN '{filter.start_date}' AND '{filter.end_date}'
        """
        if filter.production_line != 'All':
            base_query += f" AND pl.production_line_name = '{filter.production_line}'"
        
        base_query += ' GROUP BY p.product_name'
        base_query += ' ORDER BY total_ncs ASC'
        base_query += f' LIMIT {top_k}'

        data = self.connection.execute(base_query).fetchdf()

        # sort the data by total_ncs
        data = data.sort_values(by='total_ncs', ascending=False)

        return data
    
    def get_defects_distribution_by_process_step(self, filter: Filter, k: int = 5) -> pd.DataFrame:
        """
        query to get the defects distribution by process step

        Args:
        -----
        filter (Filter):
            filter object
        k (int):
            top k process steps to return

        Returns:
        --------
        pd.DataFrame:
            pd.DataFrame of the defects distribution by process step
        """
        base_query = f"""SELECT ps.process_step_name, SUM(f.qty_ncs) AS total_ncs
        FROM sink_data_mart.main.internal_ncs_fact f
            INNER JOIN sink_data_mart.main.product_dimension p
                ON f.prod_id_fk = p.product_id
            INNER JOIN sink_data_mart.main.production_line_dimension pl
                ON p.prod_line_fk = pl.production_line_id
            INNER JOIN sink_data_mart.main.process_steps_dimension ps
                ON f.process_step_fk = ps.process_step_id
        WHERE f.date BETWEEN '{filter.start_date}' AND '{filter.end_date}'
        """
        if filter.production_line != 'All':
            base_query += f" AND pl.production_line_name = '{filter.production_line}'"

        base_query += ' GROUP BY ps.process_step_name'
        base_query += ' ORDER BY total_ncs ASC'
        base_query += f' LIMIT {k}'

        data = self.connection.execute(base_query).fetchdf()

        return data
    
    def get_defects_distribution_by_issues(self, filter: Filter, k: int = 5) -> pd.DataFrame:
        """
        query to get the defects distribution by issues

        Args:
        -----
        filter (Filter):
            filter object
        k (int):
            top k issues to return

        Returns:
        --------
        pd.DataFrame:
            pd.DataFrame of the defects distribution by issues
        """
        base_query = f"""SELECT i.issue_name, SUM(f.qty_ncs) AS total_ncs
        FROM sink_data_mart.main.internal_ncs_fact f
            INNER JOIN sink_data_mart.main.product_dimension p
                ON f.prod_id_fk = p.product_id
            INNER JOIN sink_data_mart.main.production_line_dimension pl
                ON p.prod_line_fk = pl.production_line_id
            INNER JOIN sink_data_mart.main.issues_dimension i
                ON f.issues_fk = i.issue_id
        WHERE f.date BETWEEN '{filter.start_date}' AND '{filter.end_date}'
        """
        if filter.production_line != 'All':
            base_query += f" AND pl.production_line_name = '{filter.production_line}'"

        base_query += ' GROUP BY i.issue_name'
        base_query += ' ORDER BY total_ncs ASC'
        base_query += f' LIMIT {k}'

        data = self.connection.execute(base_query).fetchdf()
        return data
    
    def get_defects_distribution_by_recurring_issues(self, filter: Filter) -> pd.DataFrame:
        """
        query to get the defects distribution by 8M's root cause

        Args:
        -----
        filter (Filter):
            filter object

        Returns:
        --------
        pd.DataFrame:
            pd.DataFrame of the defects distribution by 8M's root cause
        """
        base_query = f"""SELECT i.is_recurrent, SUM(f.qty_ncs) AS total_ncs
        FROM sink_data_mart.main.internal_ncs_fact f
            INNER JOIN sink_data_mart.main.product_dimension p
                ON f.prod_id_fk = p.product_id
            INNER JOIN sink_data_mart.main.production_line_dimension pl
                ON p.prod_line_fk = pl.production_line_id
            INNER JOIN sink_data_mart.main.issues_dimension i
                ON f.issues_fk = i.issue_id
        WHERE f.date BETWEEN '{filter.start_date}' AND '{filter.end_date}'
        """
        if filter.production_line != 'All':
            base_query += f" AND pl.production_line_name = '{filter.production_line}'"

        base_query += ' GROUP BY i.is_recurrent'
        base_query += ' ORDER BY total_ncs ASC'

        data = self.connection.execute(base_query).fetchdf()
        
        # replace 1 by Yes and 0 by No
        data['is_recurrent'] = data['is_recurrent'].replace({'1': 'Yes', '0': 'No'})

        return data
    
    def get_defects_distribution_by_ishikawa_root_cause(self, filter: Filter) -> pd.DataFrame:
        """
        query to get the defects distribution by Ishikawa's root cause

        Args:
        -----
        filter (Filter):
            filter object
        k (int):
            top k 8M's root cause to return

        Returns:
        --------
        pd.DataFrame:
            pd.DataFrame of the defects distribution by Ishikawa's root cause
        """
        root_cause = ['labour', 'raw_material', 'method', 'machine', 'measure', 'env']
        ishi_data = {}
        for root in root_cause:

            base_query = f"""SELECT i.is_{root}, SUM(f.qty_ncs) AS total_ncs
            FROM sink_data_mart.main.internal_ncs_fact f
                INNER JOIN sink_data_mart.main.product_dimension p
                    ON f.prod_id_fk = p.product_id
                INNER JOIN sink_data_mart.main.production_line_dimension pl
                    ON p.prod_line_fk = pl.production_line_id
                INNER JOIN sink_data_mart.main.issues_dimension i
                    ON f.issues_fk = i.issue_id
            WHERE f.date BETWEEN '{filter.start_date}' AND '{filter.end_date}'
            """
            if filter.production_line != 'All':
                base_query += f" AND pl.production_line_name = '{filter.production_line}'"

            base_query += f' GROUP BY i.is_{root}'
            base_query += f' HAVING i.is_{root} = 1'

            data = self.connection.execute(base_query).fetchdf()

            # append the data to the ishi_data, if data is empty, append 0
            if data.empty:
                ishi_data[root] = 0
            else:
                ishi_data[root] = data.iloc[0, 1]

        # create a dataframe
        data = pd.DataFrame(ishi_data.items(), columns=['issue_name', 'total_ncs'])
        
        # sort the data by total_ncs
        data = data.sort_values(by='total_ncs')

        # calculate percentage
        data['total_ncs'] = data['total_ncs'] / data['total_ncs'].sum() * 100

        return data