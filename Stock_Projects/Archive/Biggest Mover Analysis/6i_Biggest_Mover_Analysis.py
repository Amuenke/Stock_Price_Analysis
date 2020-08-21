# Goal: 

# Date: 3/24/19

# Pseudocode:
#       Find the single biggest gainer and loser that have been indexed from each date so far
#           Cross reference _file_names.txt and _biggest_movers_archive.txt

#       Average the indexed_data for the biggest gainers and their 10 closest datasets collected from
#           error_comparison.txt

#       Average the indexed_data for the biggest losers and their 10 closest datasets collected from
#           error_comparison.txt

#       Write data set to _indexed_data_averages.txt in following format:
#           indexed_date| time| avg gainer %| avg loser %

from pprint import pprint
import numpy as np

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

# Go through each of lines and make string of date and symbol until you get a match for each row
#   Once you get a match, save index of file_name to access later
file_list = readfile('_file_names.txt')
biggest_movers_list = readfile('_biggest_movers_archive.txt')

gainer_match_list = []
loser_match_list = []
index_list = []
for line in biggest_movers_list:

    i = 0
    newline = line.split('|')
    no_row_match = True

    while no_row_match:
        compare_string = newline[0] + '_' + newline[2 + i]
        for item in file_list:
            if item[23:-5] == compare_string:
                index_list.append(i)
                if newline[1] == 'G':
                    gainer_match_list.append(item[:-1])
                else:
                    loser_match_list.append(item[:-1])
                no_row_match = False
                break                
        i += 1

        if i+2 == len(newline):
            break

gainer_addition_list = []
loser_addition_list = []

# Go through error_comparison.txt and get 10 closest datasets to those already in list. 
close_dataset_list = readfile('_error_comparison.txt')
for line in close_dataset_list:
    newline = line.split('|') # idx 0 holds original dataset and 1 holds 10 matches seperated by ','
    for file_name in gainer_match_list:
        if file_name[23:-4] == newline[0]:
            gainer_addition_list.append(newline[1][:-1])
    for file_name in loser_match_list:
        if file_name[23:-4] == newline[0]:
            loser_addition_list.append(newline[1][:-1])
            
# Add new datasets to original gainer and loser lists in file.txt format
for line in gainer_addition_list:
    newline = line.split(',')
    for date_symbol in newline:
        gainer_match_list.append('indexed_files\\_indexed_' + date_symbol + '.txt')

for line in loser_addition_list:
    newline = line.split(',')
    for date_symbol in newline:
        loser_match_list.append('indexed_files\\_indexed_' + date_symbol + '.txt')

# Omit any duplicates
gainer_match_list = list(set(gainer_match_list))
loser_match_list = list(set(loser_match_list))

# Load np data array and get an average data set using indexes of file_names for row index
data_array = np.load('_data_array.npy')

gainer_index_list = []
loser_index_list = []
for line in file_list:
    for filename in gainer_match_list:
        if line[:-1] == filename:
            gainer_index_list.append(file_list.index(line))
    for filename in loser_match_list:
        if line[:-1] == filename:
            loser_index_list.append(file_list.index(line))

gainer_average_array = np.zeros((1, 1955)) # 1 row by 1955 columns (9:31 - 16:00)
loser_average_array = np.zeros((1, 1955))
for i in gainer_index_list:
    gainer_average_array += data_array[i,:]
gainer_average_array /= len(gainer_index_list)

for i in loser_index_list:
    loser_average_array += data_array[i,:]
loser_average_array /= len(loser_index_list)

# Create a list of strings to write to file and write to file:
file_write_list = readfile('_timelist.txt')
for i in range(len(file_write_list)):
    file_write_list[i] = file_write_list[i].replace(',', '|')
    file_write_list[i] = file_write_list[i].replace('\n', '|')
    file_write_list[i] += str(round(gainer_average_array[0,i], 4))
    file_write_list[i] += '|'
    file_write_list[i] += str(round(loser_average_array[0,i],4))

writefile(file_write_list, '_indexed_data_averages.txt')
print('Data written to file.')
input('Press enter to exit.')

    
    
