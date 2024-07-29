import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY = "9WDEAGEDJB44KS0G"
NEWS_API_KEY = "4521407e98784b23bbb1fefa6bfc21d4"
TWILIO_SID = "ACfb67ae9fc94eb250fc5b354df4678d9f"
TWILIO_AUTH_TOKEN = "0d38303ea72eddb99889171f34f6098d"

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]

yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)

difference = (float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
up_down=None
if difference >0:
    up_down="increasing"
else:
    up_down="decreasing"

diff_percent =round((difference / float(yesterday_closing_price)) * 100)
print(diff_percent)

if abs(diff_percent) > 1:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
    three_articles = articles[:3]

    formatted_articles = [f"{STOCK_NAME}: {up_down} {diff_percent} Headline: {article['title']}.\nBrief: {article['description']}" for article in
                          three_articles]

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_="+12086035070",
            to="+9203156867866"
        )
        print(message.sid)
