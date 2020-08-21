from alpha_vantage.timeseries import TimeSeries
import io
import datetime 
import pprint
import time
import pandas

date = input('Date(MM.DD.YY): ')

while True:
    symbol = input("Symbol: ")
    
    if symbol == 'NEWDATE':
        date = input('Date(MM.DD.YY): ')
    else:
        ts = TimeSeries(key='5IVRPT29H0856T26', output_format='pandas')
        data, meta_data = ts.get_intraday(symbol ,interval='1min', outputsize='full')

        # Insert date of data before symbol     
        file = date + '_' + symbol + '.txt'

        export_csv = data.to_csv(file, index = True, header=True)

        print(symbol + ' recorded')
