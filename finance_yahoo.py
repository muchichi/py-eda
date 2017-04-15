#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 22:09:55 2017

@author: mussie
"""

from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd


def main():
    tickers = ['AAPL','MSFT','^GSPC']
    
    data_source = 'yahoo'
    
    start_date = '2000-01-01'
    end_date = '2016-12-31'
    
    panel_data = data.DataReader(tickers, data_source, start_date, end_date)
    
    # Get the adjusted closing price
    adj_close = panel_data.ix['Adj Close']
    
    
    # Get all weekdays between 09-01-2001 and 09-30-2001
    
    all_weekdays = pd.date_range(start=start_date,end=end_date,freq='B')
    
    
    #Align the existing prices in adj_close with the new set of dates
    adj_close = adj_close.reindex(all_weekdays)
    
    # Fill the missing value by replacing them with the latest available price for each instruments
    
    adj_close = adj_close.fillna(method='ffill')
    
    #Get MSFT time series
    msft = adj_close.ix[:,'MSFT']
    
    #Calculate the 20 and 100 dys moving averages of the closing price
    #short_rolling_msft = msft.rolling(window=30).mean()
    #long_rolling_msft = msft.rolling(window=175).mean()
    
    mat_plot_adj_close(msft)
#Plotting
def plot_adj_close():
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot(msft.index,msft,lablel='MSFT')
    ax.plot(short_rolling_msft.index,short_rolling_msft,label='20 days rolling')
    ax.plot(long_rolling_msft.index,long_rolling_msft,label='100 days rolling')
    ax.set_xlabel('Date')
    ax.set_ylabel('Adjusted closing price($)')
    ax.legend()
    
def mat_plot_adj_close(df):
    short_rolling_msft = df.rolling(window=30).mean()
    long_rolling_msft = df.rolling(window=175).mean()
    plt.plot(df.index,df,label='MSFT')
    plt.plot(short_rolling_msft.index,short_rolling_msft,label='20 days rolling')
    plt.plot(long_rolling_msft.index,long_rolling_msft,label='100 days rolling')
    plt.show()
    
if __name__ == '__main__': main()

