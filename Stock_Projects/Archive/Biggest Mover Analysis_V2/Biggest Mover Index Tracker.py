'''
Goal: To keep an index of all biggest movers and record any changes in the index between calls
        The index will be 0 for the top gainer and 199 for the top loser
            Top gainer -> Lowest Gainer -> Lowest Loser -> Top Loser

Pseudocode:
    Grab and store a list of the top movers

    Every five minutes create new list

    Compare the new indexes of the old list to the indexes in the new list and record the change for that symbol

    Print out top five movers in decreasing order

    Append new list to file with date
    
    
Date: 4/15/2019
'''
####################################################################################################

# Writes contents of list to file
def appendfile(filename, line):
    try:
        with open(filename, 'a') as f:
            f.write(line)    
    except FileNotFoundError:
        print(filename, 'not found')

# Update biggest mover file with latest data
def get_biggest_movers(url):
    symbol_string = ''
    #open with GET method
    resp=requests.get(url) 
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
    return symbol_string

####################################################################################################

import time
import requests
from bs4 import BeautifulSoup
import datetime

# Define objects and constants
gain_url = 'http://www.wsj.com/mdc/public/page/2_3021-gaincomp-gainer.html?mod=topnav_2_3021'
lose_url = 'http://www.wsj.com/mdc/public/page/2_3021-losecomp-loser.html?mod=topnav_2_3021'
compare_list = []

# Create filename
now = datetime.datetime.now()
date = now.strftime('%Y.%m.%d')
filename = 'biggest_movers_lists//' + date + '_biggest_movers.txt'

# Test file and notify user program has started up correctly
appendfile(filename, '')
print('Start!')

# Enter while loop to terminate at 4:00
while int(now.strftime('%H')) < 16 or now.strftime('%M') == '00':
    if int(now.strftime('%M')) % 2 == 0 and int(now.strftime('%H')) > 9:
        # Insert the looped code here (Will repeat every five minutes from 10 until 4)
        # Grab a new list of the data using get_biggest_mover_method which returns string
        # Create the newlist
        gain_list = get_biggest_movers(gain_url).split('|')[:-1]
        lose_list = get_biggest_movers(lose_url).split('|')[:-1]
        lose_list.reverse()

        new_list = gain_list + lose_list

        # Add data to file
        add_string = ''
        appendfile(filename, now.strftime('%I:%M'))
        for item in new_list:
            add_string += '|'
            add_string += item
        add_string += '\n'
        appendfile(filename, add_string)

        # Compare to the compare_list and find the biggest increase
        if compare_list:
            print(now.strftime('%I:%M|'), end = '')
            delta_list  = []

            # Go through compare list and try to find matches in new list
            # If a match is found, find the difference in indexes and append to delta list
            for item in compare_list:
                sym, ci = item.split('|')
                ci = int(ci) # compare index
                
                try:
                    ni = new_list.index(sym)    # new index
                except ValueError:
                    ni = 100 # If icon dissapeared it will now be between two sheets
                delta_list.append(ci - ni)
                
            for i in range(10):
                mi = delta_list.index(max(delta_list))
                delta_list[mi] = 0
                print(compare_list[mi].split('|')[0], end='|')

            print()

        compare_list = []
        # Build new compare_list from new list
        for i in range(len(new_list)):
            compare_list.append(new_list[i] + '|' + str(i))
            
        # Insert top moving stocks here
        
        time.sleep(61)
    else:
        time.sleep(10)
    now = datetime.datetime.now()

# Keep program open until user presses enter
input("\nPress enter to exit.")

      



                
