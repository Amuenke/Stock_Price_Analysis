'''
Goal: To see overall trend of a stock by looking at the prices of the data

Date: 4/29/2019

Pseudocode:
    Get price data as often as possible from API

    Store price data in a Panda dataframe or series

    Pull the latest datapoints out of Panda in order to get the 1min, 2min, 5min, etc minimums
'''
####################################################################################################
# FUNCTIONS:

# Append time and price to dataframe
def appendPrice(price, dataframeObject):
    pass

# Get min value since specific time
def getMinValue(time):
    pass


####################################################################################################

from datetime import datetime as dt
import requests
import pandas as pd
from pprint import pprint

# Define objects and constants
API_KEY = '5IVRPT29H0856T26'
API_URL = "https://www.alphavantage.co/query"
data = {"function": "GLOBAL_QUOTE", "symbol": 'AMZN', "apikey": API_KEY} 

# Get first time
now = dt.now()

# Holds time call of last item 
last_price_call = None

# Initialize Panda Dataframe with size big enough to support call every second (23400)
#   with an index for every second start at 9:30:00 and ending at 16:00:00
time_index = pd.date_range(start = '9:30',end = '16:00',freq = 'S', closed = 'left')
pprint(time_index)

price_data = pd.DataFrame(data = '0', index = time_index)

pprint(price_data)

# Begin while loop and repeat until 4
while int(now.strftime('%H%M')) < 1601:
            
    # Append price data to file every second, and wait to start until 9:30
    if now.strftime('%S') != last_price_call and int(now.strftime('%H%M')) > 929:

        # Get price
        quote = requests.get(API_URL, data).json()
        price = float(quote['Global Quote']['05. price'])

        # Append price into panda dataframe
        

        # Get min for each time set


        # Clear console
    

        # Print data to user
        

        # Update time for time checks 
        last_price_call = now.strftime('%S')

                          
    # Update time
    now = dt.now()
