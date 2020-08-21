'''
Goal: Create a program to input indexed_data_array from program 7, fill in all the blanks, then calculate the error
        between each line and the average values leading up to a greatest mover
        
Date: 03.28.19

Pseudocode:
       Create a new array of [1 column by len(_index_data_filenames.txt)]
           For each row, calculate the RMSE betweek the corresponding row in data_array and avg_array
       Finally, output the minimum 25 RMSE values to user, and record entire list in file with RMSE values
'''
##############################################################################################################

# Read data from filename and return each line as an item in a list
def readfile(filename):
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
            return lines
    except FileNotFoundError:
        return []

# Write list to a file
def writefile(write_list, filename):
    with open(filename, 'w') as f:
        for line in write_list:
            f.write(line + '\n')

# Clean up input list and return cleaned, alphabetically ordered list with no duplicates
def cleanlist(dirty_list):
    # Go through list and get rid of any spaces or newlines
    for i in range(len(dirty_list)-1, -1, -1):
        dirty_list[i] = dirty_list[i].replace('\n', '')
        dirty_list[i] = dirty_list[i].replace(' ', '')
        if dirty_list[i] == '':
            dirty_list.pop(i)

    # Sort the list and get rid of any duplicates
    clean_list = dirty_list
    clean_list = list(set(clean_list))
    clean_list.sort()
    
    return clean_list

# Create a list of times
def timelist_generator(date_list):
    time_list = []
    for index in range(len(date_list)):
        for i in range(9, 17):
            if i == 9:
                for j in range(31,61):
                    time_list.append(date_list[index] + ' 0' + str(i) + ':' + str(j) + ':00')
            elif i < 16:
                for j in range(60):
                    if j < 10:
                        time_list.append(date_list[index] + ' ' + str(i) + ':0' + str(j) + ':00')
                    else:
                        time_list.append(date_list[index] + ' ' + str(i) + ':' + str(j) + ':00')
            else:
                time = date_list[index] + ' 16:00:00'
                time_list.append(time)
    return time_list

##############################################################################################################

import numpy as np
from pprint import pprint
from math import sqrt
from statistics import mean
from alpha_vantage.timeseries import TimeSeries

# Load array of indexed files from program 7
data_array = np.load('index_data.npy')

# Alter the data array to fill all empty holes
# Go one direction and copy all data going one way
# Then go other direction with data, copying all holes the other way
file_list = readfile('_index_data_filenames.txt')
time_list = timelist_generator(['0,','1,'])
symbol_list = []
for line in file_list:
    symbol_list.append(line[9:-11])

for i in range(len(symbol_list)):
    last_price = None
    for j in range(len(time_list)):
        if data_array[i,j] == 100.:
            data_array[i,j] = last_price
        else:
            last_price = data_array[i,j]
    last_price = None
    for j in range(-1, len(time_list)-1):
        if data_array[i,j] == 100.:
            data_array[i,j] = last_price
        else:
            last_price = data_array[i,j]

#       Open up _indexed_data_averages.txt and store average gainer data for indexes 0,09:31 through 1,16:00
#        in an avg_array of [1 row x (len(list_from_0,09:31_to_1,16:00)) columns]
compare_list = []
for line in readfile('_indexed_data_averages.txt'):
    if line[0] == '0' or line[0] == '1':
        compare_list.append(line.split('|')[2])

compare_array = np.zeros((1,len(compare_list)))

for i in range(len(compare_list)):
    compare_array[0,i] = compare_list[i]

print(len(symbol_list))

#   Make new array of len(symbol_list) x 1 and store the RMSE between each row and the compare_array
rmse_array = np.zeros((len(symbol_list), 1))
for i in range(len(symbol_list)):
    calc_array = np.subtract(compare_array, data_array[i,:])
    calc_array_squared = np.square(calc_array)
    error_sum = calc_array_squared.sum()
    rmse_array[i,0] = sqrt(error_sum / len(compare_list))

min_index_list = []
for i in range(25):
    min_index_list.append(None)
    min_value = 100
    for j in range(len(symbol_list)):
        if rmse_array[j, 0] < min_value:
            min_value = rmse_array[j,0]
            min_index_list[i] = j
    rmse_array[min_index_list[i], 0] = 100
    
# Evereything after this is just for testing the results
# I want an average of 1% postive over all the data, but preferably would beat the DOW Jones
ts = TimeSeries(key='5IVRPT29H0856T26', output_format= 'pandas')

change_list =[]

for min_index in min_index_list:
    data, meta = ts.get_daily(symbol_list[min_index])
    open_price = data.loc['2019-03-29', '1. open']
    close_price = data.loc['2019-03-29', '4. close']
    percent_change = round(((close_price - open_price) / open_price) * 100 , 2)
    print(symbol_list[min_index].ljust(10), percent_change)

    change_list.append(percent_change)

print(mean(change_list))
    

