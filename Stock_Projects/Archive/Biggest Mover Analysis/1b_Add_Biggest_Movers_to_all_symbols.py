# Goal: Get all symbols available

# Date: 3/24/19


# Pseudocode:
#       Get all symbols available


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
            f.write(line)
            if '\n' not in line:
                f.write('\n')

def cleanlist(dirty_list):
    for i in range(len(dirty_list)-1, -1, -1):
        dirty_list[i] = dirty_list[i].replace('\n', '')
        dirty_list[i] = dirty_list[i].replace(' ', '')
        if dirty_list[i] == '' or ('^' in dirty_list[i]) or ('$' in dirty_list[i]) or ('~' in dirty_list[i]) or ('.' in dirty_list[i]):
            dirty_list.pop(i)

    clean_list = dirty_list
    clean_list = list(set(clean_list))
    clean_list.sort()
    
    return clean_list

# Get list of symbols from 
with open('_biggest_movers_archive.txt') as f:
    lines = f.readlines()
symbol_list = []
for line in lines:
    indiv = line.split('|')
    for i in range(2,len(indiv)):
        symbol_list.append(indiv[i])
        
all_list = readfile('_all_symbols.txt')

all_list += symbol_list
all_list = cleanlist(all_list)



print(len(all_list))

all_list.sort()
writefile(all_list, '_all_symbols.txt')

input('Press enter to exit.')



        
