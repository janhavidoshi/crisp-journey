import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('data/stocks.db')

# Create a cursor object
cur = conn.cursor()
cur1 = conn.cursor()

# Define the query
query = """
SELECT * 
FROM stock_prices 
WHERE Stock = 'AAPL' 
AND Date BETWEEN '2023-08-01' AND '2023-08-31';
"""

query1 = """
SELECT * 
FROM stock_news 
WHERE Stock = 'AAPL' 
AND datetime BETWEEN '2023-08-01' AND '2023-08-31';"""

# Execute the query
cur1.execute(query)

# Fetch all the results
results = cur1.fetchall()

# Print the results
for row in results:
    print(row)

# Execute the query
cur.execute(query1)

# Fetch all the results
results1 = cur.fetchall()

# Close the connection
conn.close()

# Print the results
for row in results1:
    print(row)