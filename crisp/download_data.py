import requests
import pandas as pd
from datetime import datetime
import finnhub
import os

# Your Finnhub API key
api_key = 'choeuuhr01qjvijljc60choeuuhr01qjvijljc6g'
finnhub_client = finnhub.Client(api_key=api_key)

# Define the stocks and the time period you are interested in
stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META']
start_date = '2022-08-01'
end_date = '2023-09-01'
start_timestamp = int(datetime.strptime(start_date, '%Y-%m-%d').timestamp())
end_timestamp = int(datetime.strptime(end_date, '%Y-%m-%d').timestamp())

# Create a data directory if it does not exist
if not os.path.exists('data'):
    os.makedirs('data')

# Download stock prices
for stock in stocks:
    data = finnhub_client.stock_candles(stock, 'D', start_timestamp, end_timestamp)
    if data['s'] == 'ok':
        df = pd.DataFrame(data)
        df['t'] = pd.to_datetime(df['t'], unit='s')
        df = df[['t', 'o', 'c']]
        df.columns = ['Date', 'Open', 'Close']
        df.to_csv(f'data/{stock}_prices.csv', index=False)
    else:
        print(f'Error downloading stock prices for {stock}.')

# Download news articles
for stock in stocks:
    data = finnhub_client.company_news(stock, _from=start_date, to=end_date)
    if data:
        df = pd.DataFrame(data)
        df['datetime'] = pd.to_datetime(df['datetime'], unit='s')
        df = df[['datetime', 'headline', 'source', 'summary', 'url']]
        df.to_csv(f'data/{stock}_news.csv', index=False)
    else:
        print(f'No news articles available for {stock} from {start_date} to {end_date}.')

print('Data downloaded successfully!')

