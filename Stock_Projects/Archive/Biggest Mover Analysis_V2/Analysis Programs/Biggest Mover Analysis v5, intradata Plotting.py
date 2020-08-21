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

# Import symbols from biggest_movers file
def get_symbols(filename):
    lines = readfile(bma_file)
    symbol_list = []
    for i in range(len(lines)-1, len(lines) - 3, -1):
        symbol_list += lines[i].split('|')[2:-1]
        
    return symbol_list

# Returns a list of the lines from given filename
def readfile(filename):
    try:
        with open(filename, 'r') as f:
            return f.readlines()
    except FileNotFoundError:
        return []

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
import matplotlib.pyplot as plt
from os import system

df = pd.read_pickle('biggest_mover_intradata\\2019.04.04_price.pkl').T
index = 0

while True:
    
    # Plot the item at the index to console
    df.iloc[1564:,index].plot()
    plt.show()


    user_input = input('A<-  ->D')
    if user_input == 'a':
        if index == 0:
            pass
        else:
            index -= 1
    elif user_input == 'd':
        index += 1
# Wait for user to press a or d to go back or go forward

      



                
