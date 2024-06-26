import duckdb
import pandas as pd

# load both dataframes
compressor_data = pd.read_csv('./data/compressor_data.csv')
maintenance_data = pd.read_csv('./data/maintenance_data.csv')

# create query - business problem

# question: what is the compressor with most maintenance notes?
query = """SELECT compressor_tag, COUNT(*) as maintenance_count
    FROM maintenance_data
    GROUP BY compressor_tag
    ORDER BY maintenance_count DESC"""

# execute the query
results = duckdb.sql(query)

print("Question: what is the compressor with most maintenance notes?")
print(results)

# question: what is the supplier with highest average maintenance cost?
query = """SELECT supplier, ROUND(AVG(maintenance_cost), 2) as avg_cost
    FROM maintenance_data JOIN compressor_data
    ON maintenance_data.compressor_tag = compressor_data.compressor_tag
    GROUP BY supplier
    ORDER BY avg_cost DESC"""

# execute the query
results = duckdb.sql(query)

print("Question: what is the supplier with highest average maintenance cost?")
print(results)

# question: what is the fluid with lowest average maintenance cost?
query = """SELECT fluid, ROUND(AVG(maintenance_cost), 2) as avg_cost
    FROM maintenance_data JOIN compressor_data
    ON maintenance_data.compressor_tag = compressor_data.compressor_tag
    GROUP BY fluid
    ORDER BY avg_cost ASC"""

# execute the query
results = duckdb.sql(query)

print("Question: what is the fluid with the lowest average maintenance cost?")
print(results)

# is there a combination of fluid and supplier that is more expensive?
query = """SELECT fluid, supplier, ROUND(AVG(maintenance_cost), 2) as avg_cost
    FROM maintenance_data JOIN compressor_data
    ON maintenance_data.compressor_tag = compressor_data.compressor_tag
    GROUP BY fluid, supplier
    ORDER BY avg_cost DESC"""

# execute the query
results = duckdb.sql(query)

print("Is there a combination of fluid and supplier that is more expensive?")
print(results)

# is there a combination of fluid and maintenance notes description that is more expensive?
query = """SELECT fluid, maintenance_description, ROUND(AVG(maintenance_cost), 2) as avg_cost
    FROM maintenance_data JOIN compressor_data
    ON maintenance_data.compressor_tag = compressor_data.compressor_tag
    GROUP BY fluid, maintenance_description
    ORDER BY avg_cost DESC
    LIMIT 5"""

# execute the query
results = duckdb.sql(query)

print("Is there a combination of fluid and maintenance notes description that is more expensive?")
print(results)

