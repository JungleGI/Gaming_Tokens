# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 09:45:22 2023

@author: Ulrich
"""

from requests import Request, Session
import json
import pandas as pd
import streamlit as st
import datetime
import time



st.title('TopCoin Tracker')

#Time input
user_date = st.date_input('Start Date', value="today")
start_time = round((time.mktime(user_date.timetuple())))*1000
end_time = round(time.mktime(datetime.datetime.now().timetuple()))*1000

#Tickers
tickers = ('12965','9674','10688','3816','9308','15585','22265','9175','11367','14783','11212','22289','12749','10631','15463','15142','2130','27445')


#Data
@st.cache_data()
def getdata(symbol,start_time,end_time):
    url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/historical'
    parameters = {
      'id':symbol,
      'time_start':start_time,
        'time_end': end_time,
        'interval':'1d'   
    }

    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': st.secrets['api_key'],
    }
    
    session = Session()
    session.headers.update(headers)
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    
    price_data=[]
    timestamp_data=[]
    ticker_data=[]
    for item in data['data']['quotes']:
        timestamp_data.append(item['timestamp'])
        price_data.append(item['quote']['USD']['price'])
        ticker_data.append(data['data']['name'])
        
    df1 = pd.DataFrame()
    df2 = pd.DataFrame()
    df3 = pd.DataFrame()
    df1['timestamp'] = pd.DataFrame(timestamp_data)
    df2['price'] = pd.DataFrame(price_data)
    df3['ticker'] = pd.DataFrame(ticker_data)
    df = pd.DataFrame()
    df = pd.concat([df1,df2,df3], axis=1)
 
    return(df)

df_price_data = pd.DataFrame()
for ticker in tickers:
    df_tmp = getdata(ticker,start_time,end_time)
    df_price_data = pd.concat([df_price_data,df_tmp])

#Formatting Data
df_price_data['timestamp'] = pd.to_datetime(df_price_data.timestamp).dt.tz_localize(None)
df_price_data['Time'] = df_price_data['timestamp'].dt.strftime('%m-%d %H:%M')
df_price_data.set_index('Time', inplace=True)
df_price_data = df_price_data[['price','ticker']]
#df_price_data.columns = ['price','ticker']
dfpd = df_price_data.pivot_table(index=['Time'],columns='ticker', values=['price'])
dfpd.columns = [col[1] for col in dfpd.columns.values]

#Calcs
df_daily_returns = dfpd.pct_change()
df_daily_returns = df_daily_returns[1:]
df_cum_daily_returns = (1 + df_daily_returns).cumprod() - 1

#Charting
Chart1 = df_cum_daily_returns[['Good Games Guild','Wilder World','Yield Guild Games','Star Atlas','SIDUS','Enjin Coin']]
Chart2 = df_cum_daily_returns[['Verasity','Vulcan Forged PYR','GuildFi','Myria','Katana Inu','GameSwift']]
Chart3 = df_cum_daily_returns[['Oasys','MOBOX','Aurory','Treasure','Nakamoto Games','Gods Unchained']]
st.line_chart(Chart1)
st.line_chart(Chart2)
st.line_chart(Chart3)




