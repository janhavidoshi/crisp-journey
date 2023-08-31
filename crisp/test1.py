import sqlite3
import pandas as pd

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

# # Print the results
# for row in results:
#     print(row)

# Execute the query
cur.execute(query1)

# Fetch all the results
results1 = cur.fetchall()


# # Print the results
# for row in results1:
#     print(row)

# Define the query
query2 = "SELECT * FROM stock_news_sentiment;"

# Execute the query
df = pd.read_sql(query2, conn)


# Print the first few rows of the DataFrame
print(df.head())

# Print the average sentiment for each stock
print(df.groupby('Stock')['sentiment'].mean())

# Close the connection
conn.close()