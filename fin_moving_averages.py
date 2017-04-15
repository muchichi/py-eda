import pandas
import datetime
from pandas_datareader import data
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
import pylab

#import plotly.plotly as py
#import plotly.graph_objs as go


from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY
from matplotlib.finance import candlestick_ohlc

import numpy as np

def fin_main():
    #google,  msft, amzn ,  apple = pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame()
    #get_stock_data(google,msft,amzn,apple)
    
    #Multiple tickers
    start = datetime.datetime(2005,1,1)
    end = datetime.date.today()
    
    google = data.DataReader('GOOG','yahoo',start,end)
    msft = data.DataReader('MSFT','yahoo',start,end)
    amzn = data.DataReader('AMZN','yahoo',start,end)
    apple = data.DataReader('AAPL','yahoo',start,end)
    
    stocks = pd.DataFrame({
        'AAPL': apple['Adj Close'],
        #'MSFT': msft['Adj Close'],
        'GOOG': google['Adj Close'],
        'AMZN': amzn['Adj Close']
    })
    #plot_data(google)
    #plot_plotly(google)
    #pandas_candlestick_ohlc(google)
    #plot_multiple_tickers(stocks)
    #stock_returns(stocks)
    #stock_change_by_day(stocks)
    moving_average(apple)
    
def get_stock_data(google,msft,amzn,apple):
    start = datetime.datetime(2017,1,1)
    end = datetime.date.today()
    
    google = data.DataReader('GOOG','yahoo',start,end)
    msft = data.DataReader('MSFT','yahoo',start,end)
    amzn = data.DataReader('AMZN','yahoo',start,end)
    apple = data.DataReader('AAPL','yahoo',start,end)
    
def plot_data(df):
    #pylab.rcParams['figure.figsizes'] = (15,9)
    df['Adj Close'].plot(grid=True)
    
def plot_plotly(df):
    data = [
            go.Scatter(x=df['Close'],y=df['Open'])
        ]
    py.plot(data)
    
def pandas_candlestick_ohlc(dat, stick = "day", otherseries = None):
    """
    :param dat: pandas DataFrame object with datetime64 index, and float columns "Open", "High", "Low", and "Close", likely created via DataReader from "yahoo"
    :param stick: A string or number indicating the period of time covered by a single candlestick. Valid string inputs include "day", "week", "month", and "year", ("day" default), and any numeric input indicates the number of trading days included in a period
    :param otherseries: An iterable that will be coerced into a list, containing the columns of dat that hold other series to be plotted as lines

    This will show a Japanese candlestick plot for stock data stored in dat, also plotting other series if passed.
    """
    mondays = WeekdayLocator(MONDAY)        # major ticks on the mondays
    alldays = DayLocator()              # minor ticks on the days
    dayFormatter = DateFormatter('%d')      # e.g., 12

    # Create a new DataFrame which includes OHLC data for each period specified by stick input
    transdat = dat.loc[:,["Open", "High", "Low", "Close"]]
    if (type(stick) == str):
        if stick == "day":
            plotdat = transdat
            stick = 1 # Used for plotting
        elif stick in ["week", "month", "year"]:
            if stick == "week":
                transdat["week"] = pd.to_datetime(transdat.index).map(lambda x: x.isocalendar()[1]) # Identify weeks
            elif stick == "month":
                transdat["month"] = pd.to_datetime(transdat.index).map(lambda x: x.month) # Identify months
            transdat["year"] = pd.to_datetime(transdat.index).map(lambda x: x.isocalendar()[0]) # Identify years
            grouped = transdat.groupby(list(set(["year",stick]))) # Group by year and other appropriate variable
            plotdat = pd.DataFrame({"Open": [], "High": [], "Low": [], "Close": []}) # Create empty data frame containing what will be plotted
            for name, group in grouped:
                plotdat = plotdat.append(pd.DataFrame({"Open": group.iloc[0,0],
                                            "High": max(group.High),
                                            "Low": min(group.Low),
                                            "Close": group.iloc[-1,3]},
                                           index = [group.index[0]]))
            if stick == "week": stick = 5
            elif stick == "month": stick = 30
            elif stick == "year": stick = 365

    elif (type(stick) == int and stick >= 1):
        transdat["stick"] = [np.floor(i / stick) for i in range(len(transdat.index))]
        grouped = transdat.groupby("stick")
        plotdat = pd.DataFrame({"Open": [], "High": [], "Low": [], "Close": []}) # Create empty data frame containing what will be plotted
        for name, group in grouped:
            plotdat = plotdat.append(pd.DataFrame({"Open": group.iloc[0,0],
                                        "High": max(group.High),
                                        "Low": min(group.Low),
                                        "Close": group.iloc[-1,3]},
                                       index = [group.index[0]]))

    else:
        raise ValueError('Valid inputs to argument "stick" include the strings "day", "week", "month", "year", or a positive integer')


    # Set plot parameters, including the axis object ax used for plotting
    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.2)
    if plotdat.index[-1] - plotdat.index[0] < pd.Timedelta('730 days'):
        weekFormatter = DateFormatter('%b %d')  # e.g., Jan 12
        ax.xaxis.set_major_locator(mondays)
        ax.xaxis.set_minor_locator(alldays)
    else:
        weekFormatter = DateFormatter('%b %d, %Y')
    ax.xaxis.set_major_formatter(weekFormatter)

    ax.grid(True)

    # Create the candelstick chart
    candlestick_ohlc(ax, list(zip(list(date2num(plotdat.index.tolist())), plotdat["Open"].tolist(), plotdat["High"].tolist(),
                      plotdat["Low"].tolist(), plotdat["Close"].tolist())),
                      colorup = "black", colordown = "red", width = stick * .4)

    # Plot other series (such as moving averages) as lines
    if otherseries != None:
        if type(otherseries) != list:
            otherseries = [otherseries]
        dat.loc[:,otherseries].plot(ax = ax, lw = 1.3, grid = True)

    ax.xaxis_date()
    ax.autoscale_view()
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

    plt.show()

def plot_multiple_tickers(stocks):
    stocks.plot(grid=True)
    stocks.plot(secondary_y = ["AAPL", "MSFT"], grid = True)
    
def stock_returns(returns):
    stock_return = returns.apply(lambda x: x/x[0])
    #stock_return.head()
    stock_return.plot(grid=True).axhline(y=1,color='black',lw=2)
    
def stock_change_by_day(changes):
    stock_change = changes.apply(lambda x: np.log(x) - np.log(x.shift(1)))
    stock_change.plot(grid=True).axhline(y=1,color='black',lw=2)
    
def moving_average(apple):
    apple["20d"] = np.round(apple["Close"].rolling(window = 20, center = False).mean(), 2)
    apple["50d"] = np.round(apple["Close"].rolling(window = 50, center = False).mean(), 2)
    apple["200d"] = np.round(apple["Close"].rolling(window = 200, center = False).mean(), 2)

    pandas_candlestick_ohlc(apple.loc['2016-01-04':'2016-08-07',:], otherseries = ["20d", "50d", "200d"])

if __name__ == '__main__': fin_main()
