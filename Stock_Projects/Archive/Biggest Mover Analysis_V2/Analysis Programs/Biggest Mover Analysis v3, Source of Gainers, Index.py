'''
Goal: To find out distribution of repeat biggest movers origins
        (gainers vs losers, high vs low index)

Date: 4/1/19
'''
###################################################################################################################

def readfile(filename):
    try:
        with open(filename, 'r') as f:
            line_list = f.readlines()
        return line_list
    except FileNotFoundError:
        return []

def writefile(write_list, filename):
    with open(filename, 'w') as f:
        for line in write_list:
            f.write(line + '\n')

def get_symbols(input_string):
    return input_string.split('|')[2:-1]

def find_matches_indexes(input_list, compare_list):
    return_list = []
    for i in range(len(input_list)):
        for c in compare_list:
            if input_list[i] == c:
                return_list.append(i)
    return return_list

def create_string(input_list):
    return_string = ''
    for i in input_list:
        return_string += str(i).rjust(2)
        return_string += ' '

    return return_string

###################################################################################################################

from pprint import pprint
from statistics import mean

file_data = readfile('biggest_movers_archive.txt')

mean_gain_index_list = []
mean_lose_index_list = []

# Look at biggest mover file from the bottom up and look for repeats
#   Show data to user
for i in range(len(file_data), 0, -2):
    #symbol_list = get_symbols(file_data[i-1])
    symbol_list = get_symbols(file_data[i-2])

    loser_list = get_symbols(file_data[i-3])
    gainer_list = get_symbols(file_data[i-4])

    gainer_index_list = find_matches_indexes(gainer_list, symbol_list)
    loser_index_list = find_matches_indexes(loser_list, symbol_list)

    print(file_data[i-1][:10])
    print(str(len(gainer_index_list)).rjust(2), 'G|', create_string(gainer_index_list), '|', round(mean(gainer_index_list),2))
    print(str(len(loser_index_list)).rjust(2), 'L|',  create_string(loser_index_list), '|', round(mean(loser_index_list), 2))
    print('*' * 100)

    mean_gain_index_list += gainer_index_list
    mean_lose_index_list += loser_index_list

print('Mean Loser Index:', round(mean(mean_lose_index_list),1), 'Mean Gainer Index:', round(mean(mean_gain_index_list), 1))

print('*' * 100)

mean_gain_index_list.sort()
mean_lose_index_list.sort()

# Create a histogram of all indexes from gainers and from losers
compare = 9
count = 0
print('Gainer histogram', len(mean_gain_index_list))
for m in mean_gain_index_list:
    if m > compare:
        print('|', round(count/len(mean_gain_index_list) * 100), '%\n', end='')
        compare += 10 
        count = 0
    print(str(m).rjust(3), end='')
    count += 1
print('|', round(count/len(mean_gain_index_list) * 100), '%')

compare = 9
count = 0
print('\n', '*' * 100, '\n\nLoser histogram', len(mean_lose_index_list))
for m in mean_lose_index_list:
    if m > compare:
        print('|', round(count/len(mean_lose_index_list) * 100), '%\n', end='')
        compare += 10
        count = 0
    print(str(m).rjust(3), end='')
    count += 1
print('|', round(count/len(mean_gain_index_list) * 100), '%')

input('Press enter to exit.')
