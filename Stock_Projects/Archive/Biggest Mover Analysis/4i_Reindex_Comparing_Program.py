# Goal: Create a 2D array that holds the RMSE between each of the reindexed outputs from program
#       3_Reindexing_Intra_Program to each other

# Date: 3/20/19

# Pseudocode:
#       Input data from file

#       Modify list to include all minutes, using last known price

#       Compare all files against each other with RMSE

#       Print out list of errors

import numpy as np
from math import sqrt
from pprint import pprint


# Read data from filename and return each line as an item in a list
def readfile(filename):
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
            return lines
    except FileNotFoundError:
        return []

#   Write list to a file
def writefile(write_list, filename):
    with open(filename, 'w') as f:
        for line in write_list:
            f.write(line + '\n')

# Read in file containing list of file names
file_list = readfile('_file_names.txt')

time_list = readfile('_timelist.txt')

data_array = np.zeros((len(file_list), len(time_list)))

# Read in each file in file_list into an array, taking average of last 4 relative %'s
# Go through time list, if index and time don't match, add time list data to index and keep previous price
file_index = 0
for filename in file_list:
    indexed_list = readfile(filename[:-1])

    last_change = 0
    file_time_index = 0
    time_index = 0
    
    for time in time_list:
        # Does date_index and time == time_list index?
        # If no, add time_list index and keep last recorded price
        # Once match  is found, look at next line in indexed_list_file.txt
    
        split_line = indexed_list[file_time_index].split(',')
        compare_string = split_line[6] + ',' + split_line[7][1:]

        if time[:-1] == compare_string:
            # Find average of the 4 changed values if all data is there, else use last known price
            if len(split_line) == 12:
                avg_change =  float(split_line[8][:-1]) + float(split_line[9][:-1])
                avg_change += float(split_line[10][:-1]) + float(split_line[11][:-2])
                avg_change /= 4

                last_change = avg_change

            # Array at postiion (filename_index, time_index) = last_change
            
            file_time_index += 1
            if file_time_index == len(indexed_list):
                file_time_index -= 1

        data_array[file_index, time_index] = last_change

        time_index += 1

    file_index += 1

print('DATA ARRAY')
pprint(data_array)

# Now that data array is full of data, calculate the RMSE between each line of data
#   and store in a new array of len(file_list) * len(file_list)
#   The diagonal will all be 0 hopefully

error_array = np.zeros((len(file_list), len(file_list)))

for row_index_1 in range(len(file_list)):
    # Go through list and calculate RMSE from data_array
    for row_index_2 in range(len(file_list)):
        row_error_array = np.subtract(data_array[row_index_1,:], data_array[row_index_2,:])
        row_error_array_squared = np.square(row_error_array)
        error_sum = np.sum(row_error_array_squared)
        error_array[row_index_1, row_index_2] = sqrt(error_sum / len(file_list))
            
print('ERROR ARRAY')
pprint(error_array)

np.save('_data_array.npy', data_array)
np.save('_error_array.npy', error_array)
        
input('Press enter to exit.')    
