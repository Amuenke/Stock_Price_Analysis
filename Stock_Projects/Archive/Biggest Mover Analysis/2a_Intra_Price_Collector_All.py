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
succesful_intra_calls_list = []

# Returns a list of the lines from given filename
def read_file(filename):
    lines = []
    try:
        with open(filename) as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = []
    return lines

# Writes contents of list to file
def write_file(filename, data_list):
    try:
        with open(filename, 'w') as f:
            for line in data_list:
                f.write(line)
                if '\n' not in line:
                    f.write('\n')
    except FileNotFoundError:
        pass

def match_finder(filename, dataFrame):
    match_list = []
    file_list = []
    dataframe_list = []
    
    try:
        lines = read_file(filename)
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
def get_intradata(symbol):
    global failed_intra_calls_list
    global succesful_intra_calls_list
    global symbol_list
    
    try:
        data, meta_data = ts.get_intraday(symbol, interval='1min', outputsize='full')
        filename = 'raw_data\\' + symbol + '_intra.txt'

        # Drop any data already in file
        data = data.drop(match_finder(filename, data))
        
        with open(filename, 'a') as f:
            data.to_csv(f, index = True, header = False)

        sort_file(filename)

        succesful_intra_calls_list.append(filename)

    except ValueError:
        # If call fails, tell user and record symbol that failed
        print('Bad Symbol'.ljust(15), end = '|')
        failed_intra_calls_list.append(symbol)
        symbol_list.remove(symbol + '\n')

# Sort file rows based on date index
def sort_file(filename):
    lines = read_file(filename)

    lines = list(set(lines))

    lines.sort()

    write_file(filename, lines)

# BEGIN PROGRAM
sort_file('_all_symbols.txt')
symbol_list = read_file('_all_symbols.txt')

print(len(symbol_list), 'items to download.', str(len(symbol_list) // 120) + '+ minutes left')

for item in symbol_list:
    time_start = time.time()
    print(item[:-1].ljust(5), end='|')
    flag = True
    count = 0
    while flag:
        try:
            get_intradata(item[:-1])
            flag = False
        except KeyError:
            time.sleep(1)
            if count > 10:
                flag = False
                failed_intra_calls_list.append(item[:-1])
                print('Key Error')
            count += 1

            
            
    print()
    time_elapsed = time.time() - time_start
    if (time_elapsed < 0.5):
        time.sleep(0.5 - time_elapsed)

write_file('_raw_intra_filenames.txt', succesful_intra_calls_list)
write_file('symbols_to_delete.txt', failed_intra_calls_list)
write_file('_all_symbols.txt', symbol_list)


input('Press enter to exit.')
