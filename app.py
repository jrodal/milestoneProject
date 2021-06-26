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

#headers
st.title('Daily Closing Values')
st.write('An Interactive Example, Using Streamlit and Bokeh')

#request user input
numStocks = None
y_scale = st.sidebar.selectbox(
    'Value scale', ['Dollar value', 'Percent Growth'])
numStocks = st.sidebar.selectbox(
    'How many stocks would you like to compare?', [1, 2, 3])
ticker1, ticker2, ticker3 = None, None, None
if numStocks:
    ticker1 = st.sidebar.text_input('Ticker symbol (e.g. UAL)')
    if numStocks>=2:
        ticker2 = st.sidebar.text_input('Ticker symbol (e.g. DAL)')
    if numStocks==3:
        ticker3 = st.sidebar.text_input('Ticker symbol (e.g. AAL)')
complete = False
complete = st.sidebar.button('Plot data')

#set up
tickersCompleted = [ticker for ticker in [ticker1, ticker2, ticker3] 
                    if ticker is not None]
colors= ['red', 'green', 'blue']

#query API and build plot
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
        try:
            data = responsedata['Time Series (Daily)']
        except KeyError:
            st.markdown('')
            st.markdown('Oops, something went wrong.')
            st.markdown('Please hit refresh and try again.')
            complete=False
            break

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
        
#display plot    
if complete:
    st.bokeh_chart(p)
complete = False
    
        






