'''
Goal: To download all intradata for biggest movers,
        and store volume and price data in two seperate panda DataFrames with the date as their name
            i.e. YYYY.MM.DD_volume.csv|YYYY.MM.DD_date.csv    

Date: 4/2/2019
'''
####################################################################################################

# Writes contents of list to file
def appendfile(filename, data_list):
    try:
        with open(filename, 'a') as f:
            line = ''
            for item in data_list:
                line += item
                line += ' '
            f.write(line)    
    except FileNotFoundError:
        pass

# gets intra data for given symbol and creates or appends file SMBL_intra.txt with data
def get_intra_data(symbol, time_list):
    price_list = []
    volume_list = []
    flag = True
    while flag:
        try:
            data, meta_data = ts.get_intraday(symbol, interval='1min', outputsize='full')
            flag = False

            # Cycle through time_list, calling 1. open and 5. volume for all matches
            # If no match, keep 4. close of last known value for price, and 0 for volume
            last_time = None
            for i in range(len(time_list)):
                time = time_list[i]
                try:
                    price_list.append(data.loc[time, '1. open'])
                    volume_list.append(data.loc[time, '5. volume'])
                    last_time = time
                except KeyError:
                    volume_list.append('0')
                    if last_time == None:
                        price_list.append('0')
                    else:
                        price_list.append(data.loc[last_time, '4. close'])
                                            
        except ValueError:
            error_message = 'Error, cannot call ' + symbol + '. Try again(y/n)? '
            if input(error_message) == 'y':
                symbol = input('What ticker would you like to try? ')
            else:
                return None
    
    return price_list, volume_list

# Import symbols from biggest_movers file
def get_symbols(filename):
    lines = readfile(bma_file)
    symbol_list = []
    for i in range(len(lines)-1, len(lines) - 3, -1):
        symbol_list += lines[i].split('|')[2:-1]
    print(len(symbol_list))
    return symbol_list

# Create timelist using the dataes given from a symbol call
def get_timelist(symbol):
    data, meta_data = ts.get_daily(symbol, outputsize='compact')
    index_list = data.index.tolist()
    date_list = []
    time_list = []
    for i in range(len(index_list), len(index_list) - 5, -1):
        date_list.append(index_list[i-1])
    for i in range(4, -1, -1):
        for h in range(9, 17):
            if h == 9:
                for m in range(31,61):
                    time_list.append(date_list[i] + ' 09:' + str(m) + ':00')
            elif h < 16:
                for m in range(60):
                    if m < 10:
                        time_list.append(date_list[i] + ' ' + str(h) + ':0' + str(m) + ':00')
                    else:
                        time_list.append(date_list[i] + ' ' + str(h) + ':' + str(m) + ':00')
            else:
                time_list.append(date_list[i] + '|16:00:00')
    return time_list

# Returns a list of the lines from given filename
def readfile(filename):
    try:
        with open(filename, 'r') as f:
            return f.readlines()
    except FileNotFoundError:
        return []

# Update biggest mover file with latest data
def update_biggest_movers(gain_url, lose_url):
    url_list = [gain_url, lose_url]
    symbol_list = readfile(bma_file)
    now = datetime.datetime.now()
    date = '20' + now.strftime('%y.%m.')
    if int(now.strftime('%H')) < 9:
        if now.strftime('%a') == 'Mon':
            date += str(int(now.strftime('%d')) - 3)
        elif now.strftime('%a') == 'Sun':
            date += str(int(now.strftime('%d')) - 2)
        else:
            date += str(int(now.strftime('%d')) - 1)
    else:
        if now.strftime('%a') == 'Sun':
            date += str(int(now.strftime('%d')) - 2)
        elif now.strftime('%a') == 'Sat':
            date += str(int(now.strftime('%d')) - 1)
        else:
            date += now.strftime('%d')
    for url in url_list:
        #open with GET method
        resp=requests.get(url) 
        symbol_string = date
        if url == gain_url:
            symbol_string += '|G|'
        else:
            symbol_string += '|L|'
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
                    symbol_string += s[s.find(')')+1:s.find('(')][::-1]
                    symbol_string += '|'
        symbol_string += '\n'
        symbol_list.append(symbol_string)

    # Sort list and write to file
    symbol_list = list(set(symbol_list))
    symbol_list.sort()
    writefile(bma_file, symbol_list, '')

    return date

# Writes contents of list to file
def writefile(filename, data_list, end):
    try:
        with open(filename, 'w') as f:
            for line in data_list:
                f.write(line + end)
    except FileNotFoundError:
        pass

####################################################################################################

from alpha_vantage.timeseries import TimeSeries
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime
from pprint import pprint

# Define objects and constants
ts = TimeSeries(key='5IVRPT29H0856T26', output_format= 'pandas')
gain_url = 'http://www.wsj.com/mdc/public/page/2_3021-gaincomp-gainer.html?mod=topnav_2_3021'
lose_url = 'http://www.wsj.com/mdc/public/page/2_3021-losecomp-loser.html?mod=topnav_2_3021'
bma_file = 'biggest_movers_archive.txt'

# Update and clean the biggest movers list
date = update_biggest_movers(gain_url, lose_url)
print('Biggest movers succefully updated!')
print('*' * 50)

# Import list of symbols from file, and sort to give user feel of where we are
symbol_list = get_symbols(bma_file)

# Get time_list from function
time_list = get_timelist('AMZN')

# For each symbol, call intradata, store volume in panda_volume and price in panda_price
price_array = []
volume_array = []
failed_symbols_list = []

# Record start time
time_start = time.time()
count = 0

for i in range(len(symbol_list)):
    # Get new intra_data
    price_list, volume_list = get_intra_data(symbol_list[i], time_list)
    
    # Update user on current symbol, get intradata and store data in respective list
    if price_list != 0:
        print(symbol_list[i].ljust(6), 'succesful!')
        price_array.append(price_list)
        volume_array.append(volume_list)
    # If call failed, remove symbol from list so it doesnt show in index
    else:
        print(symbol_list[i].ljust(6), 'unsuccesful :(')
        failed_symbols_list.append(symbol_list[i])
    # Make sure enough time has passed since initial call
    count += 1
    time_elapsed = time.time() - time_start
    if count > 120:
        if time_elapsed < 59:
            time.sleep(60 - time_elapsed)
            count = 0
            time_start = time.time()
        else:
            time_start = time.time()
            count = 0
            
for s in failed_symbols_list:
    symbol_list.remove(s)

# create and panda DataFrames
price_df = pd.DataFrame(price_array, index = symbol_list, columns = time_list)
volume_df = pd.DataFrame(volume_array, index = symbol_list, columns = time_list)

price_df.to_pickle('biggest_mover_intradata//' + date + '_price.pkl')
volume_df.to_pickle('biggest_mover_intradata//' + date + '_volume.pkl')

# Use pd.read_pickle(filename) to get file

# Keep program open until user presses enter
input("\nPress enter to exit.")

      



                
