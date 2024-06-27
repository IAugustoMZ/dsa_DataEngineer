import os
import duckdb
import numpy as np

# definitions
DATABASE_NAME = 'production.db'
DATABASE_PATH = os.path.join('.', 'data', DATABASE_NAME)

# delete the db file if it exists
if os.path.exists(DATABASE_PATH):
    os.remove(DATABASE_PATH)

# create a connection to the database
con = duckdb.connect(database=DATABASE_PATH)

# create the tables of production
# production table
con.execute("""
    CREATE TABLE production(
    order_id INTEGER PRIMARY KEY,
    product_id INTEGER,
    quantity INTEGER,
    defects INTEGER,
    defect_id INTEGER
)
""")

# product table
con.execute("""
    CREATE TABLE product(
    product_id INTEGER PRIMARY KEY,
    product_name VARCHAR,
    price FLOAT,
    production_line VARCHAR
)
""")

# defects table
con.execute("""
    CREATE TABLE defects(
    defect_id INTEGER PRIMARY KEY,
    defect_name VARCHAR
)
""")

# insert data into the tables
defects = [
    'Reactor',
    'Box Sealer',
    'Packing',
    'Packaging Production',
    'Box Coding',
    'Lung Tanks',
    'Raw Material Tanks',
    'Bottle Coding',
    'Labeling',
    'Palletizing',
    'Filling',
    'Internal Transfer'
]

# insert defects
for i, defect in enumerate(defects):
    con.execute(f"INSERT INTO defects(defect_id, defect_name) VALUES ({i}, '{defect}')")

# insert products
products = [
    ('A1', 2.5, 'A'),
    ('A2', 3.5, 'A'),
    ('A3', 4.5, 'A'),
    ('B1', 5.5, 'B'),
    ('B2', 6.5, 'B'),
    ('B3', 7.5, 'B'),
    ('C1', 8.5, 'C'),
    ('C2', 9.5, 'C'),
    ('C3', 10.5, 'C'),
    ('D1', 11.5, 'D'),
    ('D2', 12.5, 'D'),
    ('D3', 13.5, 'D'),
    ('E1', 14.5, 'E'),
    ('E2', 1.5, 'E'),
    ('E3', 16.5, 'E')
]
for i, product in enumerate(products):
    con.execute(f"INSERT INTO product(product_id, product_name, price, production_line) VALUES " + 
                f"({i}, '{product[0]}', {product[1]}, '{product[2]}')")

# insert production data
for i in range(1000):
    con.execute("INSERT INTO production(order_id, product_id, quantity, defects, defect_id) VALUES "+
                f"({i}, {np.random.randint(1, len(products)+1)}, {np.random.randint(1, 10000)}, " +
                f"{np.random.randint(0, 100)}, {np.random.randint(1, len(defects)+1)})")
    
# business question: which products have the highest defect rates?
query = """WITH CTE AS (
    SELECT product_name, 
        SUM(defects) AS total_defects,
        SUM(quantity) AS total_quantity
    FROM production JOIN product ON production.product_id = product.product_id
    GROUP BY product_name
)
SELECT product_name,
    ROUND(total_defects * 100 / total_quantity, 2) AS defect_rate
FROM CTE
ORDER BY defect_rate DESC;
"""

# run the query
result = con.execute(query).fetchall()

# print the result
print('Business Question: Which products have the highest defect rates?')
print('Product Name | Defect Rate')
print('-------------|------------')
for row in result:
    print(f'{row[0]:^13}|{row[1]:^12}')

# business question: which production lines have the highest defect cost?
query = """WITH CTE AS (
    SELECT production_line, 
        SUM(defects) AS total_defects,
        SUM(price) AS total_price
    FROM production JOIN product ON production.product_id = product.product_id
    GROUP BY production_line
)
SELECT production_line,
    ROUND(total_defects * total_price, 2) AS defect_cost
FROM CTE
ORDER BY defect_cost DESC;
"""

# run the query
result = con.execute(query).fetchall()

# print the result
print('Business Question: Which production lines have the highest defect cost?')
print('Production Line | Defect Cost')
print('----------------|------------')
for row in result:
    print(f'{row[0]:^16}|{row[1]:^12}')

# business question: which defects have the highest defect cost rates?
query = """WITH CTE AS (
    SELECT defect_name, 
        (defects * price) AS defect_cost,
        (quantity * price) AS total_cost
    FROM production JOIN product ON production.product_id = product.product_id
    JOIN defects ON production.defect_id = defects.defect_id
)
SELECT defect_name,
    ROUND(SUM(defect_cost) * 100 / SUM(total_cost), 2) AS defect_cost_rate
FROM CTE
GROUP BY defect_name
ORDER BY defect_cost_rate DESC;
"""

# run the query
result = con.execute(query).fetchall()

# print the result
print('Business Question: Which defects have the highest defect cost rates?')
print('Defect Name | Defect Cost Rate')
print('------------|------------------')
for row in result:
    print(f'{row[0]:^12}|{row[1]:^18}')

