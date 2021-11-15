import requests
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
absolute_diff = round(abs(latest_adjusted_close_data - the_day_before_latest_adjusted_close_data), 2)
diff_rate = round((absolute_diff / latest_adjusted_close_data), 2)

if diff_rate >= 0.05:
    news_response = requests.get(url=NEWS_ENDPOINT, params=news_params)
    news_data = news_response.json()["articles"][:3]
    print(news_data)


# STEP 3: Use twilio.com/docs/sms/quickstart/python
# Send a separate message with each article's title and description to your phone number. 
# HINT 1: Consider using a List Comprehension.


# Optional: Format the SMS message like this:
# """
# TSLA: 🔺2%
# Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?.
# Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to
# file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height
# of the coronavirus market crash.
# or
# "TSLA: 🔻5%
# Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?.
# Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to
# file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height
# of the coronavirus market crash.
# """

