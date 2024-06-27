import duckdb
import numpy as np

# connect with the database DuckDB in memory
# con = duckdb.connect(database=':memory:')

# if I wanted to create a database in disk:
con = duckdb.connect(database='./data/production.db')

# create a table named 'production' with columns order_id, product_id, quantity, defects
con.execute("CREATE TABLE production(order_id INTEGER, product_id INTEGER, quantity INTEGER, defects INTEGER)")

# insert some data into the table
for _ in range(1000):
    con.execute("INSERT INTO production VALUES "+
                f"({np.random.randint(1111, 999999)}, {np.random.randint(1, 10)}," + 
                f" {np.random.randint(1, 1000)}, {np.random.randint(0, 100)})")
    
# run query - which products have the highest defect amounts?
result = con.execute(
    "SELECT product_id, AVG(defects) as avg_defects FROM production GROUP BY product_id ORDER BY avg_defects DESC").fetchall()
print(result)

# export the results to a csv file
con.execute("COPY (SELECT product_id, AVG(defects) " +
            "as avg_defects FROM production GROUP BY product_id ORDER BY avg_defects DESC) TO './data/results.csv' " +
            "(HEADER, DELIMITER ',');")

# read the csv file
result = con.execute("SELECT * FROM read_csv_auto('data/results.csv')").fetchall()
print(result)
