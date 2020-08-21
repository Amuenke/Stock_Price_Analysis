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

master_list = []
symbol_list = []
g_list = []
l_list = []
for line in readfile('biggest_movers_archive.txt'):
    divide = line.split('|')
    for i in range(len(divide)-2):
        if '\n' not in divide[i+2]:
            master_list.append(divide[i+2].ljust(5) + divide[1].ljust(2) + divide[0][3:5])
            symbol_list.append(divide[i+2])
            if divide[1] == 'G':
                g_list.append(divide[i+2])
            else:
                l_list.append(divide[i+2])
                

master_list.sort()
symbol_list = list(set(symbol_list))
symbol_list.sort()
g_list = list(set(g_list))
g_list.sort()
l_list = list(set(l_list))
l_list.sort()

print('Total: ', len(master_list))
print('Diff : ', len(symbol_list))

mode_list = []
for symbol in symbol_list:
    count = 0
    for item in master_list:
        if symbol.ljust(5) in item:
            count += 1
    mode_list.append(str(count).rjust(2) + ' ' + symbol)

mode_list.sort()

for i in range(len(mode_list)-1, -1, -1):
    if ' 1' in mode_list[i]:
        mode_list.pop(i)

print('*' * 50)
print('Multis: ', len(mode_list))
print('Singles: ', len(symbol_list) - len(mode_list))

###################################################################################################################
# Going to go through program once and get a new master list of all losers turned gainers
loser_list = []
for line in readfile('biggest_movers_archive.txt'):
    divide = line.split('|')
    if divide[1] == 'L':
        for i in range(len(divide)-2):
            if '\n' not in divide[i+2]:
                loser_list.append(divide[i+2] + '_' + divide[0])
write_list = []

loser_swap_count = 0
for item in loser_list:
    symbol = item[:-9]
    day = int(item[-5:-3])
    tag = True
    for line in readfile('biggest_movers_archive.txt'):
        divide = line.split('|')        
        if int(divide[0][8:10]) > day and divide[1] == 'G':
            for i in range(len(divide)-2):
                if '\n' not in divide[i+2]:
                    if divide[i+2] == symbol and tag == True:
                        loser_swap_count += 1
                        tag = False
                        write_list.append(symbol.ljust(6) + divide[0])
print('*' * 50)
print('FORMER LOSERS:', loser_swap_count, 'out of', len(loser_list))

write_list = list(set(write_list))
write_list.sort()

writefile(write_list, 'notable_gainers.txt') 

###################################################################################################################
# Now we're going to go through again checnking for symbols and make a list of all symbols followed by any
#   gains or losses
notable_count = 0
tot_count = 0

archive_symbol_list = symbol_list
multi_g_list = []
multi_l_list = []

for idx in range(len(symbol_list)):
    length = len(symbol_list[idx])
    for line in readfile('biggest_movers_archive.txt'):
        divide = line.split('|')
        for i in range(len(divide) - 2):
            if divide[i+2] == symbol_list[idx][:length]:
                symbol_list[idx] += '|' + divide[1]
                
    new_divide = symbol_list[idx].split('|')
    flag = False
    # Start list from second item, skipping the symbol name and first 'L' or 'G' if available
    for i in range(len(new_divide)-1):
        if new_divide[i+1] == 'G':
            tot_count += 1
            if i != 0:
                notable_count += 1
                multi_g_list.append(symbol_list[idx][:length])
        if new_divide[i+1] == 'L' and i != 0:
            multi_l_list.append(symbol_list[idx][:length])
multi_g_list = list(set(multi_g_list))
multi_l_list = list(set(multi_l_list))


                
print('FORMER ANYTHING:', notable_count, 'out of', tot_count)
print('*' * 50)
print('Total Number:', len(symbol_list), '| Gainers:', len(g_list), '| Losers:', len(l_list))
print('Multi Gainers:', len(multi_g_list), '| Multi Losers:', len(multi_l_list))
print('*' * 50)
print('Chance of success:', round(float(len(multi_g_list)) / float(len(symbol_list))  * 100, 2))
print('*' * 50)

input('Press enter to exit')
