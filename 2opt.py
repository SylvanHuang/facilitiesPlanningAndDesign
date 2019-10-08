import string
import time

class solver():
    def __init__(self):

        print('''
                This is a 2 opt problem solver.\n
                Enter routings of machines by their letter without spaces... EXAMPLE: 1234\n
                Enter the volume as an integer value.\n
                Email abemery@clemson.edu with questions, comments, or concerns!\n
                ''')

        # dictionary of product information
        self.userDict = {}
        self.productCombinations = {}
        self.flows = []
        self.distances = []
        self.distanceMatrix = []
        self.machines = []
        self.smallestPenalty = 999999999
        self.foundSmaller = False

        # makes the table of products and populates it with 0s
        self.makeTable()

        self.smallestPenaltyOrder = self.machines

        self.calculateFlows()
        self.printFromTo()
        self.t = time.time()
        self.generateAllOrders()

    # gathers all of the facility information from the user
    def makeTable(self):

        # prompt the user to enter the number of products the facility makes
        numProducts = int(input('Enter the number of products:\t\t'))

        # prompt the user to enter the machines that are available
        self.machines = list(input('Enter the machines that are available separated by a comma:\t').split(','))

        # prompt the user to enter the distances between machine placements
        self.distances = list(input('Enter the distances between machine placements separated by a comma: ').split(','))

        # convert all distances to ints and store in 2d list
        for i, distance in enumerate(self.distances):
            self.distances[i] = int(self.distances[i])

        # make the flows and distance matrices
        for machine in self.machines:
            # temporary list for each row
            temp = []

            # create 2d list of machine flow values; initially populate with 0s
            for machine in self.machines:
                temp.append(0)
            self.flows.append(temp)
            self.distanceMatrix.append(temp)

        print('\n')

        # loop through and allow the user to enter all of their mahcine problems
        for i in range(0, numProducts):
            routing = input('Enter routing of product {} separated by a comma:\t\t'.format(i + 1))
            volume = int(input('Enter the volume for product {}:\t\t\t\t\t'.format(i + 1)))
            self.userDict[i] = [routing, volume]

            # formatting becuase we are IE but we aren't animals
            print('\n')

    def resetDistanceMatrix(self):
        self.distanceMatrix = []
        for machine in self.machines:
            # temporary list for each row
            temp = []

            # create 2d list of machine flow values; initially populate with 0s
            for machine in self.machines:
                temp.append(0)
            self.distanceMatrix.append(temp)

    # calculate the flows between parts
    def calculateFlows(self):
        for i, firstMachine in enumerate(self.machines):
            for j, secondMachine in enumerate(self.machines):

                # construct the query string
                queryString = firstMachine + ',' + secondMachine

                # have to construct the reverse query stirng instead of qs[::-1]
                # in case there is a machine whose alias is more than one character long
                rQueryString = secondMachine + ',' + firstMachine

                # reset the flow volume to 0
                flowVolume = 0

                for key in self.userDict:

                    # checks for the query string
                    if queryString in self.userDict[key][0]:
                        flowVolume += self.userDict[key][1]

                    # checks for the reverse fo the query string
                    if rQueryString in self.userDict[key][0]:
                        flowVolume += self.userDict[key][1]

                # don't even consider values generated when i == j
                if i != j:
                    self.flows[i][j] = flowVolume

    # print the from to chart
    def printFromTo(self):
        print('FROM - TO CHART')
        header  = '|{: ^5s}|'.format(' ')
        widthLine = ''
        row = ''

        # format the header for the products
        for machine in self.machines:
            header += ' {: ^5s}|'.format(machine)
        print(header)

        # format the line that is going to seperate rows
        for width in range(0, len(header)):
            widthLine += '-'
        print(widthLine)

        # format the row to be printed
        for i, row in enumerate(self.flows):
            row = '|{: ^5s}|'.format(self.machines[i])
            for j, column in enumerate(self.flows[i]):
                if j > i:
                    row += ' {: ^5d}|'.format(column)
                else:
                    row += ' {: ^5d}|'.format(0)
            print(row)
            print(widthLine)

    # calculate the distances between machines given the order of machines
    def calculateDistance(self, machineOrder):
        for i, firstMachine in enumerate(self.machines):
            for j, secondMachine in enumerate(self.machines):
                distance = 0
                if i != j:
                    # location of the first machine
                    fLoc = machineOrder.find(firstMachine)
                    # location of the second machine
                    sLoc = machineOrder.find(secondMachine)
                    if fLoc < sLoc:
                        for k in range(fLoc, sLoc):
                            distance += self.distances[k]
                    else:
                        for k in range(sLoc, fLoc):
                            distance += self.distances[k]

                    self.distanceMatrix[i][j] = distance

    # calculate the flow volume penalty for a given matrix
    def calculatePenalty(self, distanceMatrix):
        penaltySum = 0
        for i, row in enumerate(distanceMatrix):
            for j, distance in enumerate(row):
                if j > i:
                    flow = self.flows[i][j]
                    penaltySum += distance * flow
        return penaltySum

    # print any matrix; this will eventually consume the `printFromTo` but I don't have time right now
    def printMatrix(self, matrix):
        header  = '|{: ^5s}|'.format(' ')
        widthLine = ''
        row = ''

        # format the header for the products
        for machine in self.machines:
            header += ' {: ^5s}|'.format(machine)
        print(header)

        # format the line that is going to seperate rows
        for width in range(0, len(header)):
            widthLine += '-'
        print(widthLine)

        # format the row to be printed
        for i, row in enumerate(matrix):
            row = '|{: ^5s}|'.format(self.machines[i])
            for j, column in enumerate(matrix[i]):
                if j > i:
                    row += ' {: ^5d}|'.format(column)
                else:
                    row += ' {: ^5d}|'.format(0)
            print(row)
            print(widthLine)

    '''
    generate all orders and calculate the flow penalties
    continues to do this until the flow penalty no longer decreases
    '''

    def generateAllOrders(self):
        self.foundSmaller = False

        # the original order going into the iteration
        originalOrder = ''.join(self.smallestPenaltyOrder)

        for i, firstMachine in enumerate(self.smallestPenaltyOrder):
            for j, secondMachine in enumerate(self.smallestPenaltyOrder):
                if j < i:
                    newOrder = ''
                    for letter in self.smallestPenaltyOrder:
                        if letter == firstMachine:
                            newOrder += secondMachine

                        elif letter == secondMachine:
                            newOrder += firstMachine

                        else:
                            newOrder += letter
                    self.calculateDistance(newOrder)
                    print('\n\nORDER:\t{}'.format(newOrder))

                    self.printMatrix(self.distanceMatrix)
                    penaltySum = self.calculatePenalty(self.distanceMatrix)

                    print('TOTAL PENALTY INCURRED:\t{}'.format(penaltySum))

                    if penaltySum < self.smallestPenalty:
                        self.smallestPenalty = penaltySum
                        self.smallestPenaltyOrder = newOrder
                        self.foundSmaller = True

                self.resetDistanceMatrix()

        # print the first order of machines without changining the order
        self.calculateDistance(originalOrder)
        print('\n\nORDER:\t{}'.format(originalOrder))

        self.printMatrix(self.distanceMatrix)

        penaltySum = self.calculatePenalty(self.distanceMatrix)

        print('TOTAL PENALTY INCURRED:\t{}'.format(penaltySum))
        self.resetDistanceMatrix()

        # recursivley generate orders of machines unitl the flow cost stops decreasing
        if self.foundSmaller == True:
            print('\n\n~~~~~NEW ITERATION~~~~~\n\n')
            self.generateAllOrders()

        # print the results once there is no longer an improvement
        else:
            print('TOTAL TIME TO CALCULATE {} secs'.format(time.time() - self.t))
            print('SMALLEST PENALTY INCURRED: \t{}'.format(self.smallestPenalty))
            print('SMALLEST PENALTY ORDER:\t\t{}'.format(self.smallestPenaltyOrder))

if __name__ == '__main__':
    s = solver()
