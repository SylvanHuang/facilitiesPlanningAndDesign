import string

class solver():
    def __init__(self):

        # lol plz venmo me
        print('''
                This is a 2 opt problem solver.\n
                Enter routings of machines by their letter without spaces... EXAMPLE: 1234\n
                Enter the volume as an integer value.\n
                Email abemery@clemson.edu with questions, comments, or concerns!\n
                Venmo @rooftopandy if you want to buy me a cup of coffee. \n
                ''')

        # dictionary of product information
        self.userDict = {}
        self.products = []
        self.productCombinations = {}

        self.getUserDict()
        self.getProducts()
        self.calculateFlows()
        self.printCalculations()
        print(self.productCombinations)
        print(self.userDict)

    # gathers all of the facility information from the user
    def getUserDict(self):

        # prompt the user to enter the number of products the facility makes
        numProducts = int(input('Enter the number of products:\t\t'))

        # loop through and allow the user to enter all of their mahcine problems
        for i in range(0, numProducts):
            routing = input('Enter routing of product {}:\t\t'.format(i + 1))
            volume = int(input('Enter the volume for product {}:\t\t'.format(i + 1)))
            self.userDict[i] = [routing, volume]

            # formatting becuase we are IE but we aren't animals
            print('\n')

    def getProducts(self):
        for entry in self.userDict:
            for routing in self.userDict[entry][0]:
                for character in routing:
                    if character not in self.products:
                        self.products.append(character)

    # calculate the flows between parts
    def calculateFlows(self):
        for i in range(0, len(self.products)):
            row = []
            for j in range(1, len(self.products)):
                flowVolume = 0
                queryString = self.products[i] + self.products[j]
                for product in self.userDict:
                    if queryString in self.userDict[product][0] or queryString[::-1] in self.userDict[product][0]:
                        flowVolume += self.userDict[product][1]
                row.append(flowVolume)
            self.productCombinations[self.products[i]] = row

    def printCalculations(self):
        header  = '|{: ^5s}|'.format(' ')
        widthLine = ''
        row = ''

        # format the header for the products
        for product in self.products:
            header += ' {: ^5s}|'.format(product)
        print(header)

        # format the line that is going to seperate rows
        for width in range(0, len(header)):
            widthLine += '-'
        print(widthLine)

        # format the row to be printed
        for i, key in enumerate(self.productCombinations):
            combinations = self.productCombinations[key]
            row = '|{: ^5s}|'.format(key)
            for j, combination in enumerate(combinations):
                if i == j:
                    row += ' {: ^5d}| {: ^5d}|'.format(0, combination)
                else:
                    row += ' {: ^5d}|'.format(combination)
            print(row)
            print(widthLine)

if __name__ == '__main__':
    s = solver()
