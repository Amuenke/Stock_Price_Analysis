# Goal: Collect the list of biggest movers from a website
# Date: 3/14/2019
# Pseudocode:
#   Get url from user for list
#   Copy entire page
#   Paste to temp.txt
#   Read through file and get symbol and percent change from data
#    and add to symbol_string, volume_string and percent_string:
#       symbol_string = 'SYM1|SYM2|...'
#   Append strings to biggest_movers.txt in following format:
#       Date1|G|Symbol1|Symbol2|...
#       Date1|L|Symbol1|Symbol2|...
#       Date2|G|...
#       ...

# Using https://www.geeksforgeeks.org/reading-selected-webpage-content-using-python-web-scraping/
#   for reference
import requests 
from bs4 import BeautifulSoup
import datetime

# Strings to store data:
symbol_string = ''
url = ''


def stock_list(url):
    global symbol_string

    #open with GET method 
    resp=requests.get(url) 
          
    #http_respone 200 means OK status 
    if resp.status_code==200: 
        print("Successfully accessed webpage: ", url) 
          
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
    else: 
        print("Error")

def write_to_file():
    global symbol_string
    
    with open('_biggest_movers_archive.txt', 'a') as f:
        f.write(symbol_string + '\n')

now  = datetime.datetime.now()
date = now.strftime('%m.%d.%y')
gain_url = 'http://www.wsj.com/mdc/public/page/2_3021-gaincomp-gainer.html?mod=topnav_2_3021'
lose_url = 'http://www.wsj.com/mdc/public/page/2_3021-losecomp-loser.html?mod=topnav_2_3021'
symbol_string = date + '|G|'
stock_list(gain_url)
write_to_file()
symbol_string = date + '|L|'
stock_list(lose_url)
write_to_file()

input("Press enter to exit.")
