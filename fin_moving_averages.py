import pandas
import datetime
from pandas_datareader import data
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
import pylab

def fin_main():
    start = datetime.datetime(2004,1,1)
    end = datetime.date.today()
    
    google = data.DataReader('GOOG','yahoo',start,end)
    #type(google)
    plot_data(google)
    
def plot_data(df):
    #pylab.rcParams['figure.figsizes'] = (15,9)
    df['Adj Close'].plot(grid=True)

if __name__ == '__main__': fin_main()
