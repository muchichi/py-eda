#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 22:09:55 2017

@author: mussie
"""

from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd


tickers = ['AAPL','MSFT','^GSPC']

data_source = 'yahoo'

start_date = '2000-01-01'
end_date = '2016-12-31'

panel_data = data.DataReader(tickers, data_source, start_date, end_date)
