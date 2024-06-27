import duckdb

# connect with the database DuckDB
con = duckdb.connect(database='./data/production.db')

# business question: which products have the highest defect rates?
query = """WITH CTE AS (
    SELECT product_id, 
        SUM(defects) AS total_defects,
        SUM(quantity) AS total_quantity
    FROM production
    GROUP BY product_id
)
SELECT product_id,
    ROUND(total_defects * 100 / total_quantity, 2) AS defect_rate
FROM CTE
ORDER BY defect_rate DESC;
"""

# run the query
result = con.execute(query).fetchall()

# print the result
print('Business Question: Which products have the highest defect rates?')
print('Product ID | Defect Rate')
print('-----------|------------')
for row in result:
    print(f'{row[0]:^11}|{row[1]:^12}')
