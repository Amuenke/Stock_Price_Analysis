'''
Goal: To download all intradata for biggest movers,
        and store volume and price data in two seperate panda DataFrames with the date as their name
            i.e. YYYY.MM.DD_volume.csv|YYYY.MM.DD_date.csv    

Date: 4/2/2019
'''
####################################################################################################

# Update biggest mover file with latest data
def get_big_movers(gain_url, lose_url):
    url_list = [gain_url, lose_url]
    symbol_list = []
    for url in url_list:
        #open with GET method
        resp=requests.get(url) 
        
        #http_respone 200 means OK status 
        if resp.status_code==200: 
            # we need a parser,Python built-in HTML parser is enough . 
            soup = BeautifulSoup(resp.text,'html.parser')     
            data_buffer = []
            for link in soup.find_all('a'):
               data_buffer.append(link.get_text()[::-1])
            for i in range(len(data_buffer)):
                if '(' in data_buffer[i]:
                    s = data_buffer[i]
                    symbol_list.append(s[s.find(')')+1:s.find('(')][::-1])

    # Sort list and write to file
    symbol_list = list(set(symbol_list))
    symbol_list.sort()

    return symbol_list

# Clean symbol list of all low volume symbols to reduce time between useful API calls
def volume_filter(symbol_list):
    #Check start time
    for i in range(len(slist)-1, -1, -1):
        # Get volume for symbol
        data = { "function": "GLOBAL_QUOTE", 
                    "symbol": slist[i],
                    "apikey": API_KEY} 
        response = requests.get(API_URL, data) 
        data = response.json()
        volume = data['Global Quote']['06. volume']
        
        if int(volume) < 1000:
            # Print symbol
            slist.remove(slist[i])
            
    return symbol_list


####################################################################################################

from alpha_vantage.timeseries import TimeSeries
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pprint import pprint

# Define objects and constants
GAIN_URL = 'http://www.wsj.com/mdc/public/page/2_3021-gaincomp-gainer.html?mod=topnav_2_3021'
LOSE_URL = 'http://www.wsj.com/mdc/public/page/2_3021-losecomp-loser.html?mod=topnav_2_3021'
API_URL = "https://www.alphavantage.co/query"
API_KEY = "5IVRPT29H0856T26"

# Wait until 10 AM for biggest mover list to update
now = datetime.now()
if int(now.strftime('%H')) < 10:
    time.sleep(60)

# Create list of 200 biggest movers 
slist = get_big_movers(GAIN_URL, LOSE_URL)

# Iterate through all symbols and remove any with low average volume
slist = volume_filter(slist)

# Loop through all items in continuous loop and store %change data and compare to last known value
plist = [] # Percent list holds last known %value
flag = False

while int(now.strftime('%H')) < 16:
    #dlist= [] # Hold delta values
    for i in range(len(slist)):
        data = { "function": "GLOBAL_QUOTE", 
                    "symbol": slist[i],
                    "apikey": API_KEY} 
        response = requests.get(API_URL, data) 
        data = response.json()
        change = float(data['Global Quote']['10. change percent'][:-1])

        if flag:
#           dlist.append(change - plist[i])
            delta = change - plist[i]
            if delta > 0.5:
                print(now.strftime('%H:%M|'), slist[i])
            plist[i] = change
            
            
        else:
            plist.append(change)
#            dlist.append(0)

        time.sleep(0.5)
    now = datetime.now()
    flag = True
'''
    for i in range(5):
        d = dlist.index(max(dlist))
        print(slist[d].ljust(6), end = '|')
        dlist[d] = -100

    print()
'''

    
            
# Keep program open until user presses enter
input("\nPress enter to exit.")

      



                
