# Goal: Take data from _indexed_data_averages to compare all previously gathered intra data from
#           Find out how reliable predictions will be by testing all current 

# Date: 3/24/19


# Pseudocode:
#       Get last trading day from user in format used in raw_files, store that and day before in trading_day_list

#       Read in _raw_intra_filenames.txt into filename_list, removing the '\n' at end of each line

#       Create new array of [len(_raw_intra_filenames.txt)) x (len(list_from_0,09:31_to_1,16:00))]

#       Read in each file from filename_list:
#           Look for last shown price in trading_day[1] and record as float: current_price
#           Look for trading_day_list[0] in lines and begin averaging %change in data_array
#           Continue filling out the row,

#       Create a new array of [1 column by len(_raw_intra_filenames.txt)]
#           For each row, calculate the RMSE betweek the corresponding row in data_array and avg_array

#       Finally, output the minimum 25 RMSE values to user, and record entire list in file

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

#   Convert easily typable date into date used for indexes (MM.DD) to (YYYY-MM-DD)
def date_converter(date):
    # lotd = list of trading days
    return '2019-' + date[:2] + '-' + date[3:]

# Create a list of times
def timelist_generator(date_list):
    time_list = []
    for index in range(-1, 1):
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

#       Get last trading day from user in format used in raw_files, store that and day before in trading_day_list
trading_days = []
trading_days.append(date_converter(input('Please enter latest date (MM.DD): ')))
trading_days.append(date_converter(input('Please enter previous date (MM.DD): ')))

#       Read in _raw_intra_filenames.txt into filename_list, removing the '\n' at end of each line
filename_list = cleanlist(readfile('_raw_intra_filenames.txt'))

#       Read in each file from filename_list:
avg_price_list = []
files_to_remove = []
for filename in filename_list:

#       Look for last shown price in trading_day[0] and record as float: current_price
    avg_price = None
    for line in readfile(filename):
        if trading_days[0] in line:
            lines = line.split(',')
            if lines[4] != '0':
                avg_price = float(lines[4])
    if avg_price != None and len(readfile(filename)) > 1000 and avg_price != '0':
        avg_price_list.append(avg_price)
    else:
        files_to_remove.append(filename)
for filename in files_to_remove:
    filename_list.remove(filename)

writefile(filename_list,'_index_data_filenames.txt')

#       Create new array of [len(filename_list)) x (len(list_from_0,09:31_to_1,16:00))]
data_array = np.full((len(filename_list), len(timelist_generator(['']))), 100.)

# Create a list of dates and times to based the column indexes off of
time_list = timelist_generator(trading_days)

#   Look for trading_day_list[0] in lines and begin averaging %change in data_array
#   Continue filling out the row,
for i in range(len(filename_list)):
    print(filename_list[i][9:-10])

    for j in range(len(time_list)):
        for line in readfile(filename_list[i]):
            if time_list[j] in line:
                indiv = line.split(',')
                avg = (float(indiv[1]) + float(indiv[2]) + float(indiv[3]) + float(indiv[4])) / 4
                try:
                    change = ((avg - avg_price_list[i]) / avg_price_list[i]) * 100
                except ZeroDivisionError:
                    change = 0
                    print(filename_list[i][9:-10], 'price error')
                data_array[i][j] = float(change)

np.save('index_data.npy', data_array)

pprint(data_array)

input('Press enter to exit.')
