import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report
import sqlite3
import pickle

# Connect to the SQLite database
conn = sqlite3.connect('data/stocks.db')

# Load the data
news_df = pd.read_sql_query('SELECT datetime, Stock, sentiment FROM stock_news', conn)
prices_df = pd.read_sql_query('SELECT Date, Stock, Close FROM stock_prices', conn)

# Close the connection
conn.close()

# Convert datetime to date
news_df['datetime'] = pd.to_datetime(news_df['datetime']).dt.date
prices_df['Date'] = pd.to_datetime(prices_df['Date']).dt.date

# Merge the dataframes
merged_df = pd.merge(news_df, prices_df, left_on=['datetime', 'Stock'], right_on=['Date', 'Stock'])

# Shift the closing prices to compute the daily returns
merged_df['Prev_Close'] = merged_df.groupby('Stock')['Close'].shift(1)

# Compute the daily returns
merged_df['Return'] = (merged_df['Close'] - merged_df['Prev_Close']) / merged_df['Prev_Close']

# Create a binary target variable
merged_df['Target'] = (merged_df['Return'] > 0).astype(int)

# Drop rows with missing values
merged_df = merged_df.dropna()

# Prepare the data for the model
X = merged_df[['sentiment', 'Prev_Close']]
y = merged_df['Target']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
print('Accuracy:', accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Save the model to a file
with open('model.pkl', 'wb') as file:
    pickle.dump(model, file)