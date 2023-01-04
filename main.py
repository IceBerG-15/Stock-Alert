import requests
import datetime
from twilio.rest import  Client
import os
from dotenv import load_dotenv

load_dotenv('projects\\stock-news\\.env')

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
now=datetime.datetime.now()
previous_month=now.month-1


twilio_no=os.getenv('TWILIO_NO')
auth_token=os.getenv('AUTH_TOKEN')
account_sid=os.getenv('ACCOUNT_SID')

alphavantage_api_key=os.getenv('ALPHAVANTAGE_API_KEY')
alphavantage_api_link = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={STOCK}&interval=60min&apikey={alphavantage_api_key}'

news_api_key=os.getenv('NEWS_API_KEY')
new_api_link=f'https://newsapi.org/v2/everything?q={COMPANY_NAME}&from={now.year}-{previous_month}-{now.day}&sortBy=publishedAt&apiKey={news_api_key}'


a=now.day-1  ##getting yesterday's date
b=now.day-2  ##getting day before yesterday's date
a=f'2022-12-{a} 20:00:00'
b=f'2022-12-{b} 20:00:00'

#accessing alphavantage api for info
stock_response=requests.get(alphavantage_api_link)
stock_data=stock_response.json()['Time Series (60min)']
today=float(stock_data[a]['4. close'])
yesterday=float(stock_data[b]['4. close'])
diff_percentage=round(((today-yesterday)/today)*100,2)
if diff_percentage<0:
    ch='🔻'
else:
    ch='🔺'


if abs(diff_percentage)>1:
    
    # accessing news api for info
    news_response=requests.get(new_api_link)                         
    news_data=news_response.json()['articles'][0]                 

    #sending message to the client and updating him on the stocks
    client=Client(account_sid,auth_token)
    message = client.messages \
            .create(
                body=f"TSLA: {ch}{diff_percentage}%\nHeadline: {news_data['title']}\nBrief: {news_data['description']}",
                from_=twilio_no,
                to='+917478230626'
            )
    print(message.sid)
    

