'''
Goal: Check for repeat symbols in biggest_mover_archive.txt, looking specifically for pattern of biggest losers
        soon becoming biggest winners

Date: 3/31/19

Pseudocode:
    1. Create master list of symbol_G/L_date from text file

    2. Sort list

    3. Remove any items from list that don't show up twice

    4. Print remainder to user
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

###################################################################################################################

from pprint import pprint
from statistics import mean

symbol_list = []

print('FROM BEGINNING:')

for line in readfile('biggest_movers_archive.txt'):
    # Reset variables
    gain_list = []
    lose_list = []
    index_list = []
    g_count = 0
    l_count = 0

    # Create new list of gainers and losers and compare to current symbol_list 
    indiv = line.split('|')
    if indiv[1] == 'L':
        for i in range(len(indiv) - 2):
            lose_list.append(indiv[i+2])
        for symbol in symbol_list:
            for i in range(len(lose_list)):
                if symbol == lose_list[i]:
                    l_count += 1
                    index_list.append(i)
#        if index_list:
#            print(indiv[0], 'L', l_count, round(float(l_count) / float(len(symbol_list) + 1) * 100, 1), round(mean(index_list), 1))
    else:
        for i in range(len(indiv) - 2):
            gain_list.append(indiv[i+2])
        for symbol in symbol_list:
            for i in range(len(gain_list)):
                if symbol == gain_list[i]:
                    g_count += 1
                    index_list.append(i)
        if index_list:
            print(indiv[0], 'G', g_count, '|', round(float(g_count) / float(len(symbol_list) + 1) * 100, 1),
                  '%|', round(mean(index_list), 1), 'mean index')

    symbol_list += lose_list
    symbol_list += gain_list
    symbol_list = list(set(symbol_list))
    symbol_list.sort()

print('*' * 50)

#############################################################################################################################################

print('DAY BEFORE:')

symbol_list = []
gain_list = []
lose_list = []
percent_list = []

for line in readfile('biggest_movers_archive.txt'):
    # Reset variables

    index_list = []
    g_count = 0
    l_count = 0

    # Create new list of gainers and losers and compare to current symbol_list 
    indiv = line.split('|')
    if indiv[1] == 'L':
        for i in range(len(indiv) - 2):
            lose_list.append(indiv[i+2])
        
        symbol_list = lose_list + gain_list
        gain_list = []
        lose_list = []
    else:
        for i in range(len(indiv) - 2):
            gain_list.append(indiv[i+2])
        for symbol in symbol_list:
            for i in range(len(gain_list)):
                if symbol == gain_list[i]:
                    g_count += 1
                    index_list.append(i)
        if index_list:
            percent_list.append(float(g_count) / float(len(symbol_list)) * 100)
            print(indiv[0], 'G', g_count, '|', round(float(g_count) / float(len(symbol_list) + 1) * 100, 1),
                  '% likely|', round(mean(index_list), 1), 'mean index')

print('Average succesful percentage =', round(mean(percent_list), 1))

input('Press enter to exit.')
########################################################################################################################

