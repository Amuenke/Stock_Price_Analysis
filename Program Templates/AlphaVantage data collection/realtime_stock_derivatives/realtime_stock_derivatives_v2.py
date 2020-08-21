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
BASE_TRANSACTION = 1000.0     #How much money to invest when buying or selling stock
symbols = ['NFLX', 'NVAX', 'IMGN', 'XON']   #Symbols to analyze (max of 5)
API_URL = "https://www.alphavantage.co/query"
API_KEY = "R4H3OIAKSUN8V6OX"

# Build list to hold number of shares in possesion
number_shares = []

for symbol in symbols:  #Create list to store data for symbols
    number_shares.append(0)

#Store starting money (Get from robinhood)
cash_money = float(input('Please enter current monetary value: '))
start_money = cash_money
total_money = 0

# Define functions to sell and buy stock from total_money
def sell_stock(index, price):
    global cash_money # Need to call total_money as global variable
    if number_shares[index] != 0:
        cash_money += number_shares[index] * price
        number_shares[index] = 0

def buy_stock(index, price):
    global cash_money # Need to call total_money as global variable
    if number_shares[index] == 0:
        number_shares[index] = math.floor(BASE_TRANSACTION / price)
        cash_money -= number_shares[index] * price

# Open file to store data
now = datetime.datetime.now()
f= open(str(now.strftime("%Y.%m.%d") + '.txt'), "a+")

for symbol in symbols:
    f.write(symbol)
    f.write(',')
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
        # List of keys for each interval:
        #   1. open, 2. high, 3. low, 4. close, 5. volume

        keys = a.keys()
        break_point = 0 #break for loop after given amount of loops
        break_point_max  = PAST_DATA_POINTS + 1
        
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

        # THESE VALUES NOT CURRENTLY IN USE
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
            advice  = 'BUY'
            trend = 'UP'
            buy_stock(i, price)
        elif delta_low == 0:
            advice = 'SELL'
            trend  = 'DOWN'
            sell_stock(i, price)
        elif abs(delta_high) < abs(delta_low):
            advice = 'SELL'
            trend  = 'down'
            sell_stock(i, price)
        else:
            advice = 'BUY'
            trend = 'up'
            buy_stock(i, price)
        
        #   Print Data
        print(symbol.rjust(5), ':', trend.rjust(4), ':', advice.rjust(5), ':', str(price).rjust(8), ':', str(number_shares[i]).rjust(6))
        f.write(advice)
        f.write('|')
        total_money += price * number_shares[i] #Add current share prices to total money count
        
        #   Increase index
        i += 1

    #Calculate current value and print:
    total_money += cash_money #Add cash money to share values
    delta = total_money - start_money
    print(delta, 'D|', delta / start_money, '%|', total_money, 'T|', start_money, 'S|')
    print('*' * 80)

    now = datetime.datetime.now()

    f.write(str(total_money))
    f.write('|')
    f.write(now.strftime("%X"))
    f.write("\n")
    
    #reset total_money counter
    total_money = 0

    f.close()
    
    #   Wait one minute
    time.sleep(60 / (30 / len(symbols)))


        
        


