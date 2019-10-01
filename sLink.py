def calc(arr):

    totalSim = []

    print('LENGTH = {}'.format(len(arr)))

    for i in range(0, len(arr) - 1):

        firstMachine = arr[i]

        for j in range(i + 1, len(arr)):

            secondMachine = arr[j]

            similarity = 0
            simList = [i for i in firstMachine]

            for entry in secondMachine:

                if entry in firstMachine:
                    similarity += 1
                else:
                    simList.append(entry)
            totalSim.append((similarity / len(simList)))
    return totalSim

if __name__ == '__main__':

    print('''
    ``` Example Input```\n
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]\n
    This indicates the parts that machines 1, 2, and 3 produce! \n\n''')


    ## the array of user input
    arr = []
    machineNum = 0

    in = 1

    while in != 'exit':
        in = input('Enter the jobs for machine {}:\t'.format(machineNum))
        machineNum += 1
        arr.append(list(map(int,in.strip().split()))[:n])

    arr = input('Input the array of flow between machines to calculate similarity:\t')

    print(calc(arr))
