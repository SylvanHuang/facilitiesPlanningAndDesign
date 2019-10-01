# Andrew Emery
# IE 4650
#
import sys
import string

# the amount of products that initially enter the process
inputAmount = int(input('\n\nEnter the Input Amount:\t\t\t\t\t'))

# string of the dropout rates at every step of the process
dropouts = input('\n\nEnter dropouts for each machine d1, d2, ..., dn:\t')

# function to convert the string of dropouts to list of dropouts
def Convert(string):
    li = list(string.split(","))
    for i, entry in enumerate(li):
        li[i] = float(entry)
    return li

# list of dropouts for each step in the process
dropouts = Convert(dropouts)

# go through every step and drop out along the way
for i, dropout in enumerate(dropouts):
    output = (1 - dropout) * inputAmount
    inputAmount = output

# print our final output fromthe last machine
print('\n\nOutput Amount: \t\t\t\t\t\t{}'.format(output))
