'''
Goal: To advise limit prices based on the past 30 seconds performance of Amazon

Date: 4/22/2019
'''
####################################################################################################
# FUNCTIONS:

def appendfile(filename, addstring):
    with open(filename, 'a') as f:
        f.write(addstring + '\n')

####################################################################################################

import requests
from datetime import datetime
from time import sleep

# Define objects and constants
API_KEY = '5IVRPT29H0856T26'
API_URL = "https://www.alphavantage.co/query"
data = {"function": "GLOBAL_QUOTE", "symbol": 'AMZN', "apikey": API_KEY} 

last_time = None
now = datetime.now()
filename = now.strftime('%Y-%m-%d') + '_priceData.txt'


# Begin while loop and repeat until 4
while True:
    if last_time != now.strftime('%S'):
        last_time = now.strftime('%S') 
        # Get price
        try:
            quote = requests.get(API_URL, data).json()
            price = quote['Global Quote']['05. price']
        except (TimeoutError, KeyError, json.decoder.JSONDecodeError):
            price = 'e'
        
        current_time = now.strftime('%Y-%m-%d|%H:%M:%S')

        print(current_time, price)

        appendfile(filename, current_time + '|' + price)
    else:
        sleep(0.1)

              
    now = datetime.now()   
