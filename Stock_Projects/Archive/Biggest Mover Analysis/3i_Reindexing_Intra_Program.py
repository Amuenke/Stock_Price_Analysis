# Goal: Create a file for each biggest mover following the symbol from two days before
#       the biggest move to two days after the biggest move.

# Date: 3/20/19

# Pseudocode:
#       Input the date and symbol from _biggest_mover_list for particular symbol

#       Calculate the five dates you will be pulling intra_data for
#           Keep list of trading days in list and find index of current day, pull two before, current, and two after

#       Pull all data from SYMBL_intra.txt from 5 relevant dates

#       Add an index (0 to 4) to each line for easier accesibility

#       Find the closing price at the end of the index day 1 (closing price before biggest move)

#       Calculate and add the relative price for high, low, open and close

#       Ouput list to file in CSV format as SYMBL_intra_indexed_MM.DD.YY.txt

#       Repeat for each individual biggest mover

# Read data from filename and return each line as an item in a list
def readfile(filename):
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
            return lines
    except FileNotFoundError:
        return []

# Returns a list of all date/symbol combos on or after given date
def get_master_list(start_date, current_date):

    # List to hold all date/symbol combos
    master_list = []
    
    lines = readfile('_biggest_movers_archive.txt')

    for line in lines:
        indiv = line.split('|')
        date = indiv[0].split('.')
        month = int(date[0])
        day = int(date[1])
        year = int(date[2])

        # Check that values are in the range of data collection
        if (day >= int(start_date[3:5]) or month > int(start_date[:2])) and (day <= int(current_date[3:5])):
            for i in range(2, len(indiv)):
                new_string = indiv[0] + '_' + indiv[i]
                if indiv[i] != '\n':
                    master_list.append(new_string)

    return master_list

#   Return the five trading days around the biggest mover day, 2 before, the date, and 2 after
def get_trading_days(item):
    date = item[:8]
    # lotd = list of trading days
    lotd = ['03.11.19', '03.12.19', '03.13.19', '03.14.19', '03.15.19',
            '03.18.19', '03.19.19', '03.20.19', '03.21.19', '03.22.19',
            '03.25.19', '03.26.19', '03.27.19', '03.28.19', '03.29.19',
            '04.01.19', '04.02.19', '04.03.19', '04.04.19', '04.05.19',
            '04.08.19', '04.09.19', '04.10.19', '04.11.19', '04.12.19',
            '04.15.19', '04.16.19', '04.17.19', '04.18.19', '04.19.19',
            '04.21.19', '04.22.19', '04.23.19', '04.24.19', '04.25.19']
    
    i = lotd.index(date)
    
    return [lotd[i-2], lotd[i-1], lotd[i], lotd[i+1], lotd[i+2]]
                                
#   Pull data from SYMBL_intra.txt for each of five trading days and return the list
def get_intra_data(item, trading_days):
    data = readfile('raw_data\\' + item[9:] + '_intra.txt')
    intra_data_list = []

    for line in data:
        for date in trading_days:
            year = line[2:4]
            month = line[5:7]
            day = line[8:10]
            reformatted_date = month + '.' + day + '.' + year
            if reformatted_date == date:
                # Get rid of \n at end of each line
                intra_data_list.append(line[:-1] + ',' + str(trading_days.index(date)))
                
    return intra_data_list 

#   Calculate closing price on trading day before the biggest_mover day and return a single price
def get_reference_price(item, trading_days):
    data = readfile('raw_data\\' + item[9:] + '_daily.txt')

    for line in data:
        year = line[2:4]
        month = line[5:7]
        day = line[8:10]
        reformatted_date = month + '.' + day + '.' + year

        if reformatted_date == trading_days[1]:
            new_line = line.split(',')
            return float(new_line[4])

#   Add day index, and relative price changes to each line in intra_day
def intra_modifier(intra_data, reference_price):
    rp = reference_price
    for i in range(len(intra_data)):
        new_line = intra_data[i].split(',')
        try:
            string_addition =  ',' + new_line[0][10:-3] 
            string_addition += ',' + str(round(((float(new_line[1]) - rp)/rp) * 100, 3)) + '%'
            string_addition += ',' + str(round(((float(new_line[2]) - rp)/rp) * 100, 3)) + '%'
            string_addition += ',' + str(round(((float(new_line[3]) - rp)/rp) * 100, 3)) + '%'
            string_addition += ',' + str(round(((float(new_line[4]) - rp)/rp) * 100, 3)) + '%'
   
            intra_data[i] += string_addition

        except ZeroDivisionError:
            pass

    return intra_data

#   Write the modified intra data to a file
def file_write(data_list, filename):
    with open(filename, 'w') as f:
        for line in data_list:
            f.write(line + '\n')

##############################################################################################################

# Get current date
trading_date = input("What was the last trading day (MM.DD.YY): ")
starting_date = '03.13.19'

# Get master list of all symbol/date combos after specific date
master_list = get_master_list(starting_date, trading_date)

count = 0
file_list = []

# For each item in master_list, define the five trading days you're looking at and store in a list
for item in master_list:

    # define the five trading days you're looking at and store in a list
    trading_days = get_trading_days(item)

    # pull data from SYMBL_intra.txt for relevant days and put into a list
    intra_data = get_intra_data(item, trading_days)

    if len(intra_data) > 500:

        # Calculate closing price of data on trading day before big mover day to use as reference price
        reference_price = get_reference_price(item, trading_days)

        if reference_price != None: 

            # Add strings to intra data containing INDEX, REL OPEN CHANGE, REL CLOSE CHANGE, REL HIGH CHANGE, REL LOW CHANGE
            new_intra_data = intra_modifier(intra_data, reference_price)

            # Write new list to file
            filename = 'indexed_files\\_indexed_' + item + '.txt'
            file_write(new_intra_data, filename)

            file_list.append(filename)
            count += 1

file_write(file_list, '_file_names.txt')
print(count, 'files created.')
input("Press enter to exit.")
    
    


    
        
