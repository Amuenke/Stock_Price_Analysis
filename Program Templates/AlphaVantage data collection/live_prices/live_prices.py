# GOAL IS TO REDUCE RISK AS MUCH AS POSSIBLE FOR USER WHILE MAXIMIZING PROFITS
# Will do this by keeping track of data and advising:
#   Buy when go from stagnant to positive derivative
#   Sell when go from stagnant to negative derivative
#   Hold when continually buying or selling
import requests
import json
import alpha_vantage
import time
import math
import datetime

# Variables to Modify
symbols = ['TWI']   #Symbols to analyze
API_URL = "https://www.alphavantage.co/query"
API_KEY = "5IVRPT29H0856T26"

#List of indexes
d0  = 0 # 30  sec delta index
d1  = 0 #  1  min delta index
d3  = 0 #  3  min delta index
d5  = 0 #  5  min delta index
d10 = 0 # 10  min delta index
d15 = 0 # 15  min delta index
d30 = 0 # 30  min delta index
d1h = 0 #  1 hour delta index
d2h = 0 #  2 hour delta index

# Initialize variable to store datetime Object
now  = datetime.datetime.now()

# Initialize lists to store previous price and datetimes for derivative calculation
then  = [now for symbol in symbols]
last_price = [0 for symbol in symbols]

#Begin repeating cycle that will pull prices as fast as possible under 120 calls per minute
while True:
    # Begin for loop accesing each stock at a time:
    for i in range(0, len(symbols)):
        data = { "function": "GLOBAL_QUOTE", 
                "symbol": symbols[i],
                "apikey": API_KEY} 
        response = requests.get(API_URL, data) 
        data = response.json()
        b = (data['Global Quote'])
        now  = datetime.datetime.now()
        
        # List of keys for GLOBAL_QUOTE:
        #   01. symbol, 02. open, 03. high, 04. low, 05. price, 06. volume 
        #   07. latest trading day, 08. previous close, 09. change, 10. change percent
       
        # Store current price, high price, low price, and opening price
        price = float(b['05. price'])
        opening = float(b['02. open'])
        change = b['09. change']
        change_percent = b['10. change percent']
                
        delta_price = price - last_price[i]
        delta_time  = now - then[i]

        derivative = delta_price / delta_time.total_seconds()

        relative_derivative = (derivative / opening) * 100

        print(now.strftime('%x %X'), '|', symbols[i].rjust(5), '|', price)

        #Store current price and time for comparison
        last_price[i] = price
        then[i] = now
        
    #   Don't go over 120 calls per minute\
    print('-' * 100)
    time.sleep(float(len(symbols)) / 2)


        
        


