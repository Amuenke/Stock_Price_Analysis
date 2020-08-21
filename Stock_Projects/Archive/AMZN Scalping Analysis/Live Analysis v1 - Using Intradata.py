'''
Goal: To download AMZN intradata for past five days and run an analysis tool to see if I can
        beat the market

Date: 4/22/2019
'''
####################################################################################################
# FUNCTIONS:

# Append string to file in new line
def appendfile(append_string, filename):
    with open(filename, 'a') as f:
        f.write(append_string)
    return 0
####################################################################################################

from alpha_vantage.timeseries import TimeSeries
import pandas as pd
from datetime import datetime
import requests

# Define objects and constants
API_KEY = '5IVRPT29H0856T26'
API_URL = "https://www.alphavantage.co/query"
ts = TimeSeries(key=API_KEY, output_format= 'pandas')
data = {"function": "GLOBAL_QUOTE", "symbol": 'AMZN', "apikey": API_KEY} 

# Get first time
now = datetime.now()

# Test append function and make sure file is created correctly
filename = now.strftime('%Y-%m-%d-AMZN_RT.txt')
appendfile(('*' * 50) + '\n', filename)

# Define timeholding variables
last_intra_call = None
last_price_call = None

# Begin while loop and repeat until 4
while int(now.strftime('%H%M')) < 1601:
    # Get intradata at beginning of every minute and print reccomendations
    if now.strftime('%M') != last_intra_call:
        intradata, meta_data = ts.get_intraday('AMZN', interval='1min', outputsize='compact')
        cur_low = intradata.iloc[-1, 2]
        pas_low = intradata.iloc[-2, 2]

        if cur_low > pas_low:
            print(now.strftime('%H:%M| BUY |'), cur_low)
        else:
            print(now.strftime('%H:%M| SELL|'), cur_low)
                  
        last_intra_call = now.strftime('%M')
        
    # Append price data to file every second
    if now.strftime('%S') != last_price_call and int(now.strftime('%H%M')) > 929:

        # Get price
        quote = requests.get(API_URL, data).json()
        price = quote['Global Quote']['05. price']
        appendfile(now.strftime('%H:%M:%S| ') + price + '\n', filename) 
        
        last_price_call = now.strftime('%S')
                  
    # Update time
    now = datetime.now()
