import requests
from twilio.rest import Client
from lxml import html
import config

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

stock_params = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "apikey": config.stock_api_key
}
news_params = {
    "q": COMPANY_NAME,
    "apiKey": config.news_api_key
}

stock_response = requests.get(url=STOCK_ENDPOINT, params=stock_params)
stock_data = stock_response.json()["Time Series (Daily)"]
latest_two_days = list(stock_data.items())[:2]
latest_adjusted_close_data = float(latest_two_days[0][1]["5. adjusted close"])
the_day_before_latest_adjusted_close_data = float(latest_two_days[1][1]["5. adjusted close"])
diff = round(latest_adjusted_close_data - the_day_before_latest_adjusted_close_data, 2)
absolute_diff = abs(diff)
diff_rate = round((absolute_diff / latest_adjusted_close_data), 2)


def send_alert(news_list):
    account_sid = config.account_sid
    auth_token = config.auth_token
    client = Client(account_sid, auth_token)
    for news in news_list:
        title = html.fromstring(news["title"]).text_content()
        brief = html.fromstring(news["description"]).text_content()
        if diff >= 0:
            message = client.messages.create(
                body=f'{STOCK}: 🔺{diff_rate * 100}%\n\nHeadline: {title}\n\nBrief:{brief}',
                from_=config.send_from,
                to=config.send_to
            )
        else:
            message = client.messages.create(
                body=f'{STOCK}: 🔻{diff_rate * 100}%\n\nHeadline: {title}\n\nBrief: {brief}',
                from_=config.send_from,
                to=config.send_to
            )

    print(message.status)


if diff_rate >= 0.05:
    news_response = requests.get(url=NEWS_ENDPOINT, params=news_params)
    news_data = news_response.json()["articles"][:3]
    send_alert(news_data)
else:
    if diff >= 0:
        print('Increased less than 5%')
    else:
        print('Decreased less than 5%')
