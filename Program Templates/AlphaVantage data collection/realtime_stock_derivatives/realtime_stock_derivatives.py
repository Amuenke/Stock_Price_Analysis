# GOAL IS TO REDUCE RISK AS MUCH AS POSSIBLE FOR USER WHILE MAXIMIZING PROFITS
# Will do this by keeping track of data and advising:
#   Buy when go from stagnant to positive derivative
#   Sell when go from stagnant to negative derivative
#   Hold when continually buying or selling
import requests
import alpha_vantage
import json
import time

# Insert Wanted Tickets in symbols list
API_URL = "https://www.alphavantage.co/query"
symbols = ['NFLX', 'NVAX', 'IMGN', 'XON']



#Begin repeating cycle that will pull prices every minute:
while True:
    # Begin for loop accesing each stock at a time:
    i = 0
    # Lists to store important ticker data
    open_price = []
    high_price = []
    low_price = []
    current_price = []

    for symbol in symbols:
        #   Import stock data and get current price
        data = { "function": "TIME_SERIES_INTRADAY", 
                "symbol": symbol,
                "interval": "1min",
                "apikey": "VGJ82D76OPRX990A" } 
        response = requests.get(API_URL, data) 
        data = response.json()
        a = (data['Time Series (1min)'])
        # List of keys for each interval:
        #   1. open, 2. high, 3. low, 4. close, 5. volume

        keys = a.keys()
        break_point = 0 #break for loop after given amount of loops
        break_point_max = 6

        high_sum = 0
        low_sum = 0
        highest = 0 #highest price in range
        lowest = 100000 #lowest price in range 

        price = 0  #current price
        
        # Average together last five (?) minutes of data and compare to current price
        for key in keys:
            if break_point == break_point_max:
                break
 
            high  = float(a[key]['2. high'])
            low = float(a[key]['3. low'])

            if high > highest:
                highest = high
            if low < lowest:
                lowest = low
                
            high_sum += high
            low_sum += low

            if break_point == 0:
                price = float(a[key]['4. close']) # Try to get absolute latest price available
            break_point += 1

        high_avg = high_sum / break_point_max
        low_avg = low_sum / break_point_max

        #   Compare to recent prices and find derivative
        delta_high = highest - price
        delta_low = lowest - price

        #   Determine if user should buy, sell or hold
        #       Buy if price is at relative min
        #       Sell if price is at relative max
        #       Hold if going down or going up
        trend = ''
        advice = ''
        if delta_high == 0:
            advice  = 'BUY AND HOLD  :'
            trend = 'UP'
        elif delta_low == 0:
            advice = 'SELL NOW  :'
            trend  = 'DOWN'
        elif abs(delta_high) < abs(delta_low):
            advice = '(sell) :'
            trend  = 'down'
        else:
            advice = '(hold) :'
            trend = 'up'
        
        #   Print Data
        print(symbol.rjust(5), ':', trend.rjust(4), ':', advice.rjust(12), str(price).rjust(8))
        

        #   Increase index
        i += 1
    #   Wait one minute
    print('*' * 80)
    time.sleep(60)




    """ Taking simple data in real time
    for symbol in symbols:
        #   Import stock data and get current price
        data = { "function": "GLOBAL_QUOTE", 
                "symbol": symbol,
                "apikey": "VGJ82D76OPRX990A" } 
        response = requests.get(API_URL, data) 
        data = response.json()
        a = (data['Global Quote'])
        # List of keys:
        #   01. symbol, 02. open, 03. high, 04. low, 05. price, 06. volume 
        #   07. latest trading day, 08. previous close, 09. change, 10. change percent
       
        # Store current price, high price, low price, and opening price
        open_price.append(a['02. open'])
        high_price.append(a['03. high'])
        low_price.append(a['04. low'])
        current_price.append(a['05. price'])
        
        #   Compare to recent prices and find derivative
        #   Display recent max and mins
        #   Determine if user should buy, sell or hold
        #       Buy if price is at relative min
        #       Sell if price is at relative max
        #       Hold if going down or going up

        #   Store data to print this cycle
        

        #   Increase index
        i += 1
        #   Wait one minute
        time.sleep(60)
"""
