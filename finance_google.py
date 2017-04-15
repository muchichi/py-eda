#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 23:06:13 2017

@author: mussie
"""

#from pandas_datareader import data
import pandas_datareader.data as dt

def main():
    start_date ='2017-01-01' #datetime.datetime(2017,1,1)
    end_date = '2017-03-01' #datetime.datetime(2017,3,1)
    
    ticker = ['GOOG','AAPL','AMZN','KO','PEP']
    
    dfs = dt.DataReader(ticker,'google',start_date,end_date)
    #stock_g = data.get_quote_google(ticker)
    op = df.ix['Close']

if __name__ == '__main__':main()