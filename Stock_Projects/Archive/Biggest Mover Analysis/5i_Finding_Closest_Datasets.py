# Goal: Compare the errors found in program 4 and return the data sets with 
#       the lowest RMSE score to each file for further manipulation

# Date: 3/24/19

# Pseudocode:
#       Input error_array from _error_array.npy

#       Input filename list from _file_names.txt

#       Go through each row and keep track of 5 lowest error values (not includiing the error against self)

#       Print to user and file the filename, and then the date and symbol of 5 closese datasets

import numpy as np
from io import BytesIO
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

error_array = np.load('_error_array.npy')

# Now go through each of the rows and get the 5 lowest values.
#       Print the closest matches and save to a file for future viewing

min_array = np.zeros((20,len(file_list)))

for row_index in range(len(file_list)):
    for i in range(11):
        min_value = np.min(error_array[row_index, :])
        min_index = np.argmin(error_array[row_index, :])
        error_array[row_index, min_index] = 1000
        if i != 0:
            min_array[i-1, row_index] = min_index
            min_array[i+9, row_index] = min_value

# Write results to file _error_comparison.txt        
file_write_list = []
file_write_index_list =[]
for i in range(len(file_list)):
    string_line = file_list[i][23:-5] + '|'
    index_string_line = file_list[i][23:-5].ljust(15) + '|'
    for j in range(10):
        if j != 0:
            string_line += ','
            index_string_line += '|'
        string_line += file_list[int(min_array[j, i])][23:-5]
        index_string_line += str(int(min_array[j,i])).rjust(3)
        index_string_line += str(round(min_array[j+10,i],2)).rjust(6)
    file_write_list.append(string_line)
    file_write_index_list.append(index_string_line)

writefile(file_write_list, '_error_comparison.txt')
writefile(file_write_index_list, '_error_comparison_indexes.txt')

print('Error comparison files created.')

input('Press enter to exit.')
