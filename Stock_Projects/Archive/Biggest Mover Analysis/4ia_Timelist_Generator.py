# Goal: Create a 2D array that holds the RMSE between each of the reindexed outputs from program
#       3_Reindexing_Intra_Program to each other

# Date: 3/20/19

# Pseudocode:
#       Input data from file

#       Modify list to include all minutes, using last known price

#       Compare all files against each other with RMSE

#       Print out list of errors

#   Write list to a file
def writefile(write_list, filename):
    with open(filename, 'w') as f:
        for line in write_list:
            f.write(line + '\n')
            
with open('_timelist.txt', 'w') as f:
    for k in range(5):
        for i in range(9, 17):
            if i == 9:
                for j in range(31,61):
                    time = '0' + str(i) + ':' + str(j)
                    f.write(str(k) + ',' + time + '\n')
            elif i < 16:
                for j in range(60):
                    if j < 10:
                        time = str(i) + ':0' + str(j)
                        f.write(str(k) + ',' + time + '\n')
                    else:
                        time = str(i) + ':' + str(j)
                        f.write(str(k) + ',' + time + '\n')

            else:
                f.write(str(k) + ',16:00\n')
