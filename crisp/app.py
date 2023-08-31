from flask import Flask, render_template, request
import requests
import pandas as pd
import joblib
from datetime import datetime, timedelta
from transformers import BertTokenizer, BertForSequenceClassification
from torch.nn.functional import softmax
import torch

app = Flask(__name__, template_folder='templates')

# Load the trained model
model = joblib.load('model.pkl')

# Load pre-trained model and tokenizer
tokenizer = BertTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
model_bert = BertForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    # Get the stock ticker from the form
    stock = request.form['stock']

    # Get the current date and start date
    current_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d')

    # Get the latest news from Finnhub API
    api_key = 'choeuuhr01qjvijljc60choeuuhr01qjvijljc6g'
    url = f'https://finnhub.io/api/v1/company-news?symbol={stock}&from={start_date}&to={current_date}&token={api_key}'
    response = requests.get(url)
    if response.status_code != 200:
        return render_template('index.html', suggestion='Error: Unable to fetch data from Finnhub')

    news = response.json()
    if not news:
        return render_template('index.html', suggestion='No news available for the past month')

    # Get the previous day's closing price from Finnhub API
    url = f'https://finnhub.io/api/v1/quote?symbol={stock}&token={api_key}'
    response = requests.get(url)
    quote = response.json()
    prev_close = quote['pc']

    # Preprocess the news
    news_df = pd.DataFrame(news)
    news_df['datetime'] = pd.to_datetime(news_df['datetime'], unit='s').dt.date
    news_df['sentiment'] = news_df['summary'].apply(get_sentiment)

    # Use the latest news for prediction
    latest_news = news_df.iloc[0]

    # Make a prediction
    X = latest_news[['sentiment']]
    X['Prev_Close'] = prev_close
    X = X.values.reshape(1, -1)
    prediction = model.predict(X)
    prediction = prediction.mean()

    # Suggest an action
    if prediction < 0.4:
        suggestion = 'Sell'
    elif prediction > 0.6:
        suggestion = 'Buy'
    else:
        suggestion = 'Hold'

    return render_template('index.html', suggestion=suggestion, stock=stock)


def get_sentiment(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
    outputs = model_bert(**inputs)
    probs = softmax(outputs.logits, dim=-1)
    sentiment = torch.argmax(probs, dim=-1).item()
    return sentiment


if __name__ == '__main__':
    app.run(debug=True)
