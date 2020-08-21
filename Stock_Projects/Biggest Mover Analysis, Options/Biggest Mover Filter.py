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


# Update biggest mover file with latest data
def get_biggest_movers(url):
    symbol_string = ''
    #open with GET method
    resp=requests.get(url) 
    #http_respone 200 means OK status 
    if resp.status_code==200: 
        # we need a parser,Python built-in HTML parser is enough . 
        soup = BeautifulSoup(resp.text,'html.parser')
        table = soup.find_all('div')
            
        pprint(table)
        company_names = []
        

        pprint(company_names)
    return symbol_string
            
'''        for i in range(len(data_buffer)):
            if '(' in data_buffer[i]:
                s = data_buffer[i]
                symbol_string += s[s.find('(')+1:s.find(')')]
                symbol_string += '|'
'''   

####################################################################################################

import requests
from bs4 import BeautifulSoup
from pprint import pprint

# Define objects
url = 'https://www.wsj.com/market-data/stocks/us/movers'

get_biggest_movers(url)

# Keep program open until user presses enter
input("\nPress enter to exit.")

      



                
