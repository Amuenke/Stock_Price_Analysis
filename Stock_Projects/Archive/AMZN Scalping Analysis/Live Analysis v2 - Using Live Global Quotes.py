'''
Goal: To advise limit prices based on the past 30 seconds performance of Amazon

Date: 4/22/2019
'''
####################################################################################################
# FUNCTIONS:

####################################################################################################

from datetime import datetime
import requests
import statistics

symbol = input('Symbol?: ')

# Define objects and constants
API_KEY = '5IVRPT29H0856T26'
API_URL = "https://www.alphavantage.co/query"
data = {"function": "GLOBAL_QUOTE", "symbol": symbol, "apikey": API_KEY} 

# Get first time
now = datetime.now()

# Define timeholding and index variables
last_price_call = None
i = 0

# Initialize list for holding all data
slist = []
mlist = []
for i in range(30):
    slist.append(0)
    mlist.append(0)

# Begin while loop and repeat until 4
while int(now.strftime('%H%M')) < 1601:
            
    # Append price data to file every second
    if now.strftime('%S') != last_price_call :#and int(now.strftime('%H%M')) > 929:

        # Get price
        quote = requests.get(API_URL, data).json()
        price = float(quote['Global Quote']['05. price'])

        slist[i] = price

        center = statistics.mean(slist)
        med = statistics.median(slist)

        skew = center - med

        mlist[i] = skew

        dev = statistics.stdev(slist)
            

        lr = center - (0.5 * dev)
        hr = center + (0.5 * dev)

        print_string = str(round(price,2)) + ' | ' + str(round(skew,2)) + ' | ' + str(round(dev,2))
        print(print_string)
        
        last_price_call = now.strftime('%S')

        i += 1
        if i == 30:
            i = 0
                  
    # Update time
    now = datetime.now()
