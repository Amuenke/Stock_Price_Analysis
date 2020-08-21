'''
Goal: To download AMZN intradata for past five days and run an analysis tool to see if I can
        beat the market

Date: 4/22/2019
'''
####################################################################################################

# buy share of stock
def buy(price):
    global own_stock
    global count
    global data
    if own_stock == False:
        own_stock = True
        count += 1
        return -price
    else:
        return 0
        

# sell share of stock
def sell(price):
    global own_stock
    global count
    global data
    if own_stock == True:
        own_stock = False
        count += 1
        return price
    else:
        return 0

####################################################################################################

from alpha_vantage.timeseries import TimeSeries
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime
from pprint import pprint

# Define objects and constants
ts = TimeSeries(key='5IVRPT29H0856T26', output_format= 'pandas')

# Download Amazon intradata
data, meta_data = ts.get_intraday('AMZN', interval='1min', outputsize='full')

# Go through Amazon intradata and sell and buy based on specific criteria
delta = 0.
open_price = data.iloc[0, 0]
close_price = close_price = data.iloc[len(data.index.tolist())-1, 3]
own_stock = False
count = 0

for i in range(0, len(data.index.tolist()), 1):
    if i == 0:
        pass
    else:
        ch = float(data.iloc[i-1, 1])
        cl = float(data.iloc[i-1, 2])
        ph = float(data.iloc[i-2, 1])
        pl = float(data.iloc[i-2, 2])


        if cl > pl:
            delta += buy(data.iloc[i, 2])
        elif cl < pl:
            delta += sell(data.iloc[i, 1])
        
if own_stock == True:
    delta += sell(close_price)

        

# Print scalping results compared to actual results over five days
print('Market:', round(close_price - open_price, 2))
print('Scalp :', round(delta, 2))
print('Total Transactions:', count/ 5, 'per day')
