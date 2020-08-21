# Goal is to keep track of entered stocks, give user easy to see micro plots,
    # and to record as many price and time data stamps as possible to be easily
    # imported into excel with

import os
import requests
import time
import datetime
import colorama

# Lists to hold respective data for outputting to user and file
prices = []
change_percents = []
volumes = []
past_prices = []

# Variables to Modify
symbols = ['CRCM', 'NYNY', 'BA', 'AMTBB', 'XBIT', 'ARA', 'MSC', 'PT', 'ERII', 'LAIX', 'RIGL', 'JKS', 'GTT', 'NVEE', 'JCP', 'FRTA', 'AMAG', 'PTE', 'AA', 'ORGO']   #Symbols to analyze
API_URL = "https://www.alphavantage.co/query"
API_KEY = "5IVRPT29H0856T26"

# Global variables
call_per_minute = None

# Function that will get data from Alpha_Vantage and store data within list to be accessed later
def api_request():
    for i in range(0, len(symbols)):
        data = { "function": "GLOBAL_QUOTE", 
                    "symbol": symbols[i],
                    "apikey": API_KEY} 
        response = requests.get(API_URL, data) 
        data = response.json()
        temp_stock_data = (data['Global Quote'])
        
        # List of keys for GLOBAL_QUOTE:
            #   01. symbol, 02. open, 03. high, 04. low, 05. price, 06. volume 
            #   07. latest trading day, 08. previous close, 09. change, 10. change percent
        
        change_percents[i] = temp_stock_data['10. change percent']
        prices[i] = temp_stock_data['05. price']
        volumes[i] = temp_stock_data['06. volume']

def derivatives(minutes, i, index):
    if len(past_prices[i]) > (calls_per_min * minutes):
        delta =  float(prices[i]) - float(past_prices[i][index-int((calls_per_min * minutes))])
        return str(round(delta, 2)).rjust(10)
    else:
        return ''
            

# Make lists the same length as the number of symbols to store, and output header
header = 'Time|'

for i in range(0, len(symbols)):
    change_percents.append(None)
    prices.append(None)
    volumes.append(None)
    past_prices.append([]) #Store past prices for derivative information

    symbol = symbols[i]

    # Make header string to be printed later
    header_addition = symbol + '_Price|' + symbol + '_%Change|' + symbol + '_Volume|'
    header += header_addition

# Get current date, create file with current date, and output header
now  = datetime.datetime.now()

filename = now.strftime('%Y.%m.%d') + '.txt'
with open(filename, 'a') as f:
    f.write(header + '\n') 

# Index to store past prices
index = 0

# Calculate how many calls to make a minute for calculations
time_delay = len(symbols) / 2    
calls_per_min = int(60/time_delay)

#Begin repeating cycle that will pull prices as fast as possible under 120 calls per minute (300 calls for another $50/month)
while True:
    # Fill lists with up to minute price data 
    api_request()
    now  = datetime.datetime.now()

    # Calculate time delay
    
    # Build file_string (Needs to be able to be imported into excel, give as much information as possible)
    # Also build user string

    user_string = 'Ticker:'.rjust(6) + 'Price:'.rjust(10) + '30 sec:'.rjust(10) + '1 min:'.rjust(10) + '2 min:'.rjust(10) + '5 min:'.rjust(10) + '10 min:'.rjust(10) + '15 min:'.rjust(10) + '30 min:'.rjust(10) +'\n'
    user_string += '-' * 76
    user_string += '\n'
    
    file_string = None

    file_string = now.strftime('%X') + '|'
    for i in range(0, len(symbols)):
        file_string_addition = prices[i] + '|' + change_percents[i] + '|' + volumes[i] + '|'
        file_string += file_string_addition
        
        user_string_addition = symbols[i].rjust(6) + ':' + str(prices[i]).rjust(10) + ' '
        user_string += user_string_addition

        # Store price data in past prices list
        past_prices[i].append(prices[i])

        #Swap out with functions 
        user_string += derivatives(0.5, i, index)
        user_string += derivatives(1, i, index)
        user_string += derivatives(2, i, index)
        user_string += derivatives(5, i, index)
        user_string += derivatives(10, i, index)
        user_string += derivatives(15, i, index)
        user_string += derivatives(30, i, index)
        
        user_string += '\n'
        user_string += '-' * 76
        user_string += '\n'
        
    # Output data to file
    with open(filename, 'a') as f:
        f.write(file_string + '\n')

    # Output data to user so it constantly replaces data on console
    user_string += now.strftime('%X')
    os.system('cls')
    print(user_string, flush = True)
    

    #   Don't go over 120 calls per minute
    time.sleep(time_delay)

    index += 1

        
        


