import duckdb
import pandas as pd

# load both dataframes
compressor_data = pd.read_csv('./data/compressor_data.csv')
maintenance_data = pd.read_csv('./data/maintenance_data.csv')

# create query - business problem

# question: what are the min, max and avg maintenance costs by each compressor?
query = """SELECT compressor_tag, ROUND(MIN(maintenance_cost), 2) as min_cost,
        ROUND(MAX(maintenance_cost), 2) as max_cost, 
        ROUND(AVG(maintenance_cost), 2) as avg_cost 
    FROM maintenance_data
    GROUP BY compressor_tag
    ORDER BY avg_cost DESC"""

# execute the query
results = duckdb.sql(query).df()

print("Question: what are the min, max and avg maintenance costs by each compressor?")
print(results)