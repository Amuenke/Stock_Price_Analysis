# Goal: Collect the list of biggest movers from file and then get intradata for each one
#       Store data for each one in a file of its respective symbol (i.e. AMZN.txt)
#       Only append data that is not currently in file
#           i.e. Day 1 record 5 days, Day 2 records 1 day, Day 3 records 1 day
# Date: 3/16/2019
# Pseudocode:
#   Get all symbols from text file with list of biggest movers
#       Readlines and find data matching date
#       Split line based on '|' character
#       Ignore first two entries which contain date and G or L tag
#       Ignore final entry which is '/n'
#       Ignore any bad entries (containing and non_uppercase letters)
#       Store all applicable entries in symbol_list
#
#   Sort symbol_list alphabetically
#
#   Delete any repeats from list
#
#   Call and store intradata for each symbol in 'SMBL_intra.txt'
#       Call intradata for each symbol and store as a pandas DataFrame
#       Compare indexes in DataFrame to those in file if it exists
#       Only append DataFrame data with indexes not currently in file
#       Resort file if any of DataFrame data added was out of order
#
#   Call and store daily data for each symbol in 'SMBL_daily.txt'
#       Call daily_data for each symbol and store as a pandas DataFrame
#       Compare indexes in DataFrame to those in file if it exists
#       Only append DataFrame data with indexes not currently in file
#       Resort file if any of DataFrame data was added out of order


from alpha_vantage.timeseries import TimeSeries
import time
import pandas

# Define object to call stock data from
ts = TimeSeries(key='5IVRPT29H0856T26', output_format= 'pandas')

# Lists to hold data
failed_intra_calls_list = []
failed_daily_calls_list = []

# Returns a list of the lines from given filename
def file_reader(filename):
    lines = []
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines.append('No File ' + filename)
    return lines

# Writes contents of list to file
def file_writer(filename, data_list):
    try:
        with open(filename, 'w') as f:
            for line in data_list:
                if line != '\n':
                    f.write(line)
    except FileNotFoundError:
        pass

# Checks for matches between pandas Dataframe and file and returns a list of matches
def match_finder(filename, dataFrame):
    match_list = []
    file_list = []
    dataframe_list = []
    
    try:
        lines = file_reader(filename)
        # Get list of indexes already in file
        for line in lines:
            file_list.append(line.split(',')[0])
        # Get list of indexes in new DataFrame
        dataframe_list = dataFrame.index.tolist()

        # Create list of all matching indexes between two lists
        for date in dataframe_list:
            for index in file_list:
                if index == date:
                    match_list.append(index)
    except FileNotFoundError:
        pass

    return match_list

# gets intra data for given symbol and creates or appends file SMBL_intra.txt with data
def get_intra_data(symbol):
    global failed_intra_calls_list
    
    try:
        data, meta_data = ts.get_intraday(symbol, interval='1min', outputsize='full')
        filename = symbol + '_intra.txt'

        data = data.drop(match_finder(filename, data))
        
        with open(filename, 'a') as f:
            data.to_csv(f, index = True, header = False)

        file_sort(filename)

        print('Intra Succesful', end = '|')

    except ValueError:
        # If call fails, tell user and record symbol that failed
        print('Intra Failed.ljust(15)', end = '|')
        failed_intra_calls_list.append(symbol)

# gets daily data for given symbol and creates or appends file SMBL_data.txt with data
def get_daily_data(symbol):
    global failed_daily_calls_list
    
    try:
        data, meta_data = ts.get_daily(symbol, outputsize='full')
        filename = symbol + '_daily.txt'

        data = data.drop(match_finder(filename, data))
        
        with open(filename, 'a') as f:
            data.to_csv(f, index = True, header = False)

        file_sort(filename)

        print('Daily Succesful', end = '|')

    except ValueError:
        # If call fails, tell user and record symbol that failed
        print('Daily Failed.ljust(15)', end = '|')
        failed_daily_calls_list.append(symbol)

# Sort file rows based on date index
def file_sort(filename):
    lines = file_reader(filename)

    lines.sort()

    file_writer(filename, lines)

# Import symbols from biggest_movers file
def import_symbols(filename):

    symbol_list = []

    lines = file_reader(filename)
        
    # Seperate file in seperate symbols)
    for line in lines:
        line_split = line.split('|')
        for i in range(2, len(line_split)):
            if line_split[i] != '\n':
                symbol_list.append(line_split[i])

    # Sort symbols alphabetically
    symbol_list.sort()

    # Remove any duplicates
    repeats_index_list = []
    for i in range(1, len(symbol_list)):
        if symbol_list[i] == symbol_list[i-1]:
            repeats_index_list.append(i)
    repeats_index_list.sort(reverse = True)
    for index in repeats_index_list:
        symbol_list.pop(index)

    return symbol_list
    
# MAIN PROGRAM
# Import list of symbols from file
symbol_list = import_symbols('0_biggest_movers_archive.txt')

# For each symbol call for intra and daily data
for symbol in symbol_list:
    time_start = time.time()
    print(symbol.ljust(5), end = '|')
    get_intra_data(symbol)
    get_daily_data(symbol)
    time_elapsed = time.time() - time_start
    if (time_elapsed < 1):
        time.sleep(1 - (time.time() - time_start))

    print(str(round(time_elapsed * (len(symbol_list) - symbol_list.index(symbol)) / 60, 2)).ljust(6), 'min remaining')    
    

print(failed_intra_calls_list)
print(failed_daily_calls_list)


        



                
