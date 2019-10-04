import string

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
        self.machines = ''
        self.lowestPenalty = []

        self.makeTable()
        self.calculateFlows()
        self.printFromTo()
        self.generateAllOrders()

    # gathers all of the facility information from the user
    def makeTable(self):

        # prompt the user to enter the number of products the facility makes
        numProducts = int(input('Enter the number of products:\t\t'))

        # prompt the user to enter the machines that are available
        self.machines = input('Enter the machines that are available:\t')

        # prompt the user to enter the distances between machine placements
        self.distances = list(input('Enter the distances between machine placements separated by a comma: ').split(','))
        for i, distance in enumerate(self.distances):
            self.distances[i] = int(self.distances[i])
        print(self.distances)

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
            routing = input('Enter routing of product {}:\t\t'.format(i + 1))
            volume = int(input('Enter the volume for product {}:\t\t'.format(i + 1)))
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
                queryString = firstMachine + secondMachine
                flowVolume = 0
                for key in self.userDict:
                    # checks for the query string
                    if queryString in self.userDict[key][0]:
                        flowVolume += self.userDict[key][1]
                    # checks for the reverse fo the query string
                    if queryString[::-1] in self.userDict[key][0]:
                        flowVolume += self.userDict[key][1]

                # don't even consider values generated when i == j
                if i != j:
                    self.flows[i][j] = flowVolume

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

    def generateAllOrders(self):

        for i, firstMachine in enumerate(self.machines):
            for j, secondMachine in enumerate(self.machines):
                if j < i:
                    newOrder = ''
                    for letter in self.machines:
                        if letter == firstMachine:
                            newOrder += secondMachine

                        elif letter == secondMachine:
                            newOrder += firstMachine

                        else:
                            newOrder += letter
                    self.calculateDistance(newOrder)
                    print('\n\nORDER:\t{}'.format(newOrder))

                    self.printMatrix(self.distanceMatrix)
                    print('TOTAL PENALTY INCURRED:\t{}'.format(self.calculatePenalty(self.distanceMatrix)))
                self.resetDistanceMatrix()

        # print the first order of machines without changining the order
        self.calculateDistance(self.machines)
        print('\n\nORDER:\t{}'.format(self.machines))

        self.printMatrix(self.distanceMatrix)
        print('TOTAL PENALTY INCURRED:\t{}'.format(self.calculatePenalty(self.distanceMatrix)))
        self.resetDistanceMatrix()

if __name__ == '__main__':
    s = solver()
