# GOAL IS TO REDUCE RISK AS MUCH AS POSSIBLE FOR USER WHILE MAXIMIZING PROFITS
# Will do this by keeping track of data and advising:
#   Buy when go from stagnant to positive derivative
#   Sell when go from stagnant to negative derivative
#   Hold when continually buying or selling
import requests
import alpha_vantage
import json
import time
import math
import datetime

# Variables to Modify
PAST_DATA_POINTS = 5    #How many minutes we look back for averages
BASE_TRANSACTION = 2000.0     #How much money to invest when buying or selling stock
symbols = ['DF', 'BE', 'FELP', 'SE', 'HA', 'PLCE']   #Symbols to analyze (max of 5)
API_URL = "https://www.alphavantage.co/query"
API_KEY = "5IVRPT29H0856T26"

# Build list to hold number of shares in possesion
number_shares = []

for symbol in symbols:  #Create list to store data for symbols
    number_shares.append(0)

#Store starting money (Get from robinhood)
cash_money = float(input('Please enter current monetary value: '))
start_money = cash_money #Store initial cash value to compare against at end of day
total_money = 0

# Define functions to sell and buy stock from cash_money
def sell_stock(index, price):
    global cash_money # Need to call cash_money as global variable
    if number_shares[index] != 0:
        cash_money += number_shares[index] * price
        number_shares[index] = 0

def buy_stock(index, price):
    global cash_money # Need to call cash_money as global variable
    if number_shares[index] == 0:
        number_shares[index] = math.floor(BASE_TRANSACTION / price)
        cash_money -= number_shares[index] * price

# Open file to store data
now = datetime.datetime.now()
f= open(str(now.strftime("%Y.%m.%d") + '.txt'), "a+")

for symbol in symbols:
    f.write(symbol)
    f.write('|')
f.write('\n')

        
#Begin repeating cycle that will pull prices every minute:
while True:
    f= open(str(now.strftime("%Y.%m.%d") + '.txt'), "a+")
    
    # Begin for loop accesing each stock at a time:
    i = 0
    for symbol in symbols:
        #   Import stock data and get current price
        data = { "function": "TIME_SERIES_INTRADAY", 
                "symbol": symbol,
                "interval": "1min",
                "apikey": API_KEY} 
        response = requests.get(API_URL, data) 
        data = response.json()
        a = (data['Time Series (1min)'])
        keys = a.keys()
        # List of keys for TIME_SERIES_INTRADAY
        #   1. open, 2. high, 3. low, 4. close, 5. volume

        data = { "function": "GLOBAL_QUOTE", 
                "symbol": symbol,
                "apikey": API_KEY} 
        response = requests.get(API_URL, data) 
        data = response.json()
        b = (data['Global Quote'])
        
        # List of keys for GLOBAL_QUOTE:
        #   01. symbol, 02. open, 03. high, 04. low, 05. price, 06. volume 
        #   07. latest trading day, 08. previous close, 09. change, 10. change percent
       
        # Store current price, high price, low price, and opening price
        price = float(b['05. price'])
        
        break_point = 0 #break for loop after given amount of loops
        break_point_max  = PAST_DATA_POINTS
        
        high_sum = 0
        low_sum = 0
        highest = 0 #highest price in range
        lowest = 100000 #lowest price in range 

        # Average together last five (?) minutes of data and compare to current price
        for key in keys:
            if break_point == break_point_max:
                break
 
            high = float(a[key]['2. high'])
            low = float(a[key]['3. low'])

            if high > highest:
                highest = high
            if low < lowest:
                lowest = low
                
            high_sum += high
            low_sum += low

            break_point += 1

        # THESE VALUES NOT CURRENTLY IN USE
        high_avg = high_sum / break_point_max
        low_avg = low_sum / break_point_max
        med_avg = (high_avg + low_avg) / 2

        #   Determine if user should buy, sell or hold
        #       Buy if price is at relative min
        #       Sell if price is at relative max
        #       Hold if going down or going up
        trend = ''
        advice = ''
        if price > highest:
            advice  = 'BUY'
            trend = 'BFR'
            buy_stock(i, price)
        else:
            advice = 'SELL'
            trend = 'SUBMARINE'
            sell_stock(i, price)
        
        #   Print Data to console
        print(symbol.rjust(5), '|', advice.rjust(4), '|', trend.rjust(12), '|', str(round(price, 2)).rjust(8),
              '|', str(number_shares[i]).rjust(6), "shares")
        f.write(advice)
        f.write('|')

        # Update total_money based on shares bought and value
        total_money += price * number_shares[i]
        
        #   Increase index
        i += 1
    # Write time to file
    now = datetime.datetime.now()
    f.write(str(round(total_money, 2)))
    f.write('|')
    f.write(now.strftime('%X'))
    f.write("\n")
    
    #Calculate current value and print:
    total_money += cash_money #Add cash money to share values
    delta = total_money - start_money
    print(round(delta, 2), 'D|', round((delta / start_money) * 100, 2), '%|', round(total_money, 2), 'T|', round(start_money, 2), 'S|', now.strftime("%X"))
    print('*' * 50)

   
    
    #reset total_money counter
    total_money = 0

    f.close()
    
    #   Don't go over 30 calls per minute
    time.sleep(len(symbols))


        
        


