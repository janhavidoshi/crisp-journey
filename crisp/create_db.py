import pandas as pd
from sqlalchemy import create_engine
from crisp import download_data


# Define database name and tables
database_name = 'data/stocks.db'
prices_table = 'stock_prices'
news_table = 'stock_news'

# Create an SQLite engine
engine = create_engine(f'sqlite:///{database_name}')


# Define a function to convert CSV files to SQLite tables
def convert_csv_to_sqlite(csv_file, table_name, stock):
    # Read CSV file
    df = pd.read_csv(csv_file)
    # Add a column for the stock ticker
    df['Stock'] = stock
    # Append DataFrame to SQLite table
    df.to_sql(table_name, engine, index=False, if_exists='append')


# Convert downloaded CSV files to SQLite tables
for stock in download_data.stocks:
    # Convert stock prices CSV to SQLite table
    csv_file = f'data/{stock}_prices.csv'
    convert_csv_to_sqlite(csv_file, prices_table, stock)

    # Convert stock news CSV to SQLite table
    csv_file = f'data/{stock}_news.csv'
    convert_csv_to_sqlite(csv_file, news_table, stock)

print('Data converted to SQLite tables successfully!')