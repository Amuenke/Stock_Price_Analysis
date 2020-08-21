# Create a list of times
def timelist_generator(date_list):
    time_list = []
    for index in range(len(date_list)):
        for i in range(9, 17):
            if i == 9:
                for j in range(31,61):
                    time_list.append(date_list[index] + '|0' + str(i) + ':' + str(j) + ':00')
            elif i < 16:
                for j in range(60):
                    if j < 10:
                        time_list.append(date_list[index] + '|' + str(i) + ':0' + str(j) + ':00')
                    else:
                        time_list.append(date_list[index] + '|' + str(i) + ':' + str(j) + ':00')
            else:
                time = date_list[index] + '|16:00:00'
                time_list.append(time)
    return time_list

# Write list to a file
def writefile(write_list, filename):
    with open(filename, 'w') as f:
        for line in write_list:
            f.write(line + '\n')
###########################################################################################################
from pprint import pprint

time_list = timelist_generator(['0','1'])

delta = 3. / len(time_list)

origin = -3.

new_compare_list = []
for time in time_list:
    new_compare_list.append(time + '|' + str(origin))
    origin += delta

writefile(new_compare_list, '_indexed_data_averages.txt')
