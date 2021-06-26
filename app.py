#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 25 13:18:36 2021

@author: jocelyn
"""

import requests
import pandas as pd
import bokeh as b
import bokeh.plotting as bp
import streamlit as st
import json

st.title('Daily Closing Values')

st.write('An Interactive Example, Using Streamlit and Bokeh')

#st.header('Please Type in Up to 3 Stock Ticker (e.g. AMZN)')

numStocks = None

y_scale = st.sidebar.selectbox(
    'Value scale', ['Dollar value', 'Percent Growth'])
#st.sidebar.header('How many stocks would you like to compare?')
numStocks = st.sidebar.selectbox(
    'How many stocks would you like to compare?', [1, 2, 3])

ticker1, ticker2, ticker3 = None, None, None
if numStocks:
    #st.sidebar.header('Please Input Your Stock Tickers')
    ticker1 = st.sidebar.text_input('Ticker symbol (e.g. UAL)')
    if numStocks>=2:
        ticker2 = st.sidebar.text_input('Ticker symbol (e.g. DAL)')
    if numStocks==3:
        ticker3 = st.sidebar.text_input('Ticker symbol (e.g. AAL)')

complete = False
complete = st.sidebar.button('Plot data')

tickersCompleted = [ticker for ticker in [ticker1, ticker2, ticker3] 
                    if ticker is not None]

colors= ['red', 'green', 'blue']

#if len(tickersCompleted) == numStocks:
if complete:
    
    timeSampling = 'TIME_SERIES_DAILY'
    key = '2H1YICB3NNJQ4WRX'
    p = bp.figure(title="Daily Closing Values", x_axis_type='datetime', 
                  y_axis_label= y_scale)
    
    for i,ticker in enumerate(tickersCompleted):
        url = ('https://www.alphavantage.co/query?function='
               +timeSampling+'&symbol='+ticker+'&apikey='+key)

        response = requests.get(url)

        responsedata = response.json()
        #metadata = responsedata['Meta Data']
        data = responsedata['Time Series (Daily)']

        df = pd.DataFrame.from_dict(data).T
        df.index = pd.to_datetime(df.index)
        closingValues = df['4. close'].astype(float)
        if y_scale == 'Dollar value':
            y = closingValues
        else:
            initialValue = closingValues[-1]
            y = closingValues/initialValue
        
        p.line(df.index, y, legend_label=ticker, 
                line_color=colors[i])
        
    # item_text = json.dumps(b.embed.json_item(p, 'my_plot'))
    # item = JSON.parse(item_text);
    # b.embed.embed_item(item, 'my_plot')
    #st.write(p)
    #bp.show(p)
    
    y_scale, numStocks, ticker1, ticker2, ticker3, tickersCompleted, complete, data, df, y, response, responsedata, url = None, None, None, None, None, None, None, None, None, None, None, None, None

    st.bokeh_chart(p)
    
        






