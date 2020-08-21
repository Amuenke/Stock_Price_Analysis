'''
Goal: To visualize the relative movement of prices prior to a biggest gainer or biggest loser day

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
    date = '20' + datetime.datetime.now().strftime('%y.%m.%d')
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
               data_buffer.append(link.get_text())
            for i in range(len(data_buffer)):
                if '(' in data_buffer[i]:
                    s = data_buffer[i]
                    symbol_string += s[s.find('(')+1:s.find(')')]
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
bma_file = 'biggest_movers_archive.txt'

# Read data in from biggest mover file
data = readfile(bma_file)

# Determine the biggest losers and biggest gainers for each date
for i in range(len(data)-1, -1, -2):
    date = data[i].split('|')[0]

    new_gain_list = data[i-1].split('|')[2:-1]
    new_lose_list = data[i].split('|')[2:-1]

    
    compare_list = data[i-2].split('|')[2:-1]
    compare_list += data[i-3].split('|')[2:-1]

    if i > 2:
 
        gain_match_list = []
        lose_match_list = []

        for c in compare_list:
            for g in new_gain_list:
                if g == c:
                    gain_match_list.append(g)
            for l in new_lose_list:
                if l == c:
                    lose_match_list.append(l)
            
        # For each date, get daily data for each biggest gainer and biggest loser, displaying the 10 days leading up
        #   to the biggest move for all gainers, then all losers, for that date. Then print the average change of
        #   gainers and losers for a more direct comparison
        date_list = []
        daily_array, meta_data = ts.get_daily('AMZN')
        index_list = daily_array.index.tolist()
        starting_index = index_list.index(date.replace('.', '-'))
        for j in range(10, -1, -1):
            date_list.append(index_list[starting_index - j])
        print('*' * 100)

        print(date[5:10].center(6), end = '|')
        for j in range(9, -1, -1):
            if j == 0:
                print('0'.center(7), end = '|\n')
            else:
                print(('-' + str(j)).center(7), end = '|')
        print('*' * 87)

        avg_gainer_list = []
        avg_loser_list = []

        for x in range(11):
            avg_gainer_list.append(0)
            avg_loser_list.append(0)
        
        for g in gain_match_list:
            print(g.ljust(6), end = '|')
            daily_array, meta_data = ts.get_daily(g)
            for d in range(1, len(date_list)):
                try:
                    percent_change = daily_array.loc[date_list[d], '4. close'] - daily_array.loc[date_list[d-1], '4. close']
                    percent_change /= daily_array.loc[date_list[d-1], '4. close']
                    percent_change *= 100
                    print(str(round(percent_change)).rjust(7), end = '|')
                    avg_gainer_list[d] += percent_change
                except KeyError:
                    print('0'.rjust(7), end='|')
            print('')

        print('*' * 87)
          
        for l in lose_match_list:
            print(l.ljust(6), end = '|')
            daily_array, meta_data = ts.get_daily(l)
            for d in range(1, len(date_list)):
                try:
                    percent_change = daily_array.loc[date_list[d], '4. close'] - daily_array.loc[date_list[d-1], '4. close']
                    percent_change /= daily_array.loc[date_list[d-1], '4. close']
                    percent_change *= 100
                    print(str(round(percent_change)).rjust(7), end = '|')
                    avg_loser_list[d] += percent_change
                except KeyError:
                    print('0'.rjust(7), end='|')
            print('')

        print('*' * 87)
        gainer_string = 'GAINER|'
        loser_string = 'LOSER |'
        for d in range(1, len(date_list)):
            gainer_string += str(round(avg_gainer_list[d] / 10)).rjust(7)
            loser_string += str(round(avg_loser_list[d] / 10)).rjust(7)
            gainer_string += '|'
            loser_string += '|'

        print(gainer_string + '\n' + loser_string)

# Keep program open until user presses enter
input("\nPress enter to exit.")

      



                
