from alpha_vantage.timeseries import TimeSeries
import json
import pprint

date = input('Date(MM.DD.YY): ')

while True:
    symbol = input("Symbol: ")
    
    if symbol == 'NEWDATE':
        date = input('Date(MM-DD-YY): ')
    else:
        ts = TimeSeries(key='5IVRPT29H0856T26', output_format= 'json')
        data, meta_data = ts.get_intraday(symbol = 'AAPL' ,interval='1min', outputsize='full')

        # Export full data set     
        filename = date + '_' + symbol + '.txt'
        export_csv = data.to_csv(filename, index = True, header=True)

        # Export limited data set for Excel
            # Change panda data set to only keep data for given day, and only keep time in first column
    
        #filename = date + '_' + symbol + '.txt'
        

        print(symbol + ' recorded')

