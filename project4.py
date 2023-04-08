# Name: Aiden Nelson
# SIUE EID: 800742353
# Date of Start: 4/5/2023
# Date of Completion: 4/8/2023

# This program will calculate the optimal solution to a knapsack problem using a dynamic programming approach.

from os.path import isfile

class Item:
    def __init__(self, weight, value):
        self.weight = weight
        self.value = value
        
class Cell:
    def __init__(self, value, direction):
        self.value = value
        self.direction = direction

def computeTable(items, W):
    # Create table with Cell objects initialized to 0
    table = [[Cell(0, "none") for i in range(W+1)] for j in range(len(items)+1)]
    
    # Fill in table with optimal values via dynamic programming
    for i in range(1, len(items)+1):
        for w in range(1, W+1):
            if items[i-1].weight > w:
                # If the object is too heavy to fit in the knapsack, then the optimal value is the value of the cell below
                # ie: don't take the object
                table[i][w] = Cell(table[i-1][w].value, "up")
                table[i][w].direction = "up"
            else:
                if table[i-1][w].value > table[i-1][w-items[i-1].weight].value + items[i-1].value:
                    # If the value of the cell below is greater than the value of the current item plus the diagonal
                    # then the optimal value is the value of the cell below
                    table[i][w] = Cell(table[i-1][w].value, "up")
                    table[i][w].direction = "up"
                else:
                    # If the value of the cell below is less than the value of the current item plus the diagonal
                    # then the optimal value is the value of the current item plus the diagonal
                    table[i][w] = Cell(table[i-1][w-items[i-1].weight].value + items[i-1].value, "diagonal")

    return table


def printOptimalSolution(table, items, W):
    # Print out optimal solution
    print("\nThe optimal knapsack solution with a weight of ", W, " has value of ", table[len(items)][W].value, " and involves item(s) {", sep="", end="")

    i = len(items)
    w = W

    result = ""
    # Go through table, include item if it has a diagonal direction
    while i > 0 and w > 0:
        if table[i][w].direction == "diagonal":
            w -= items[i-1].weight
            result += str(i) + ", "
        i -= 1

    # Remove last comma and space
    result = result[:-2]

    # Print out result
    print(result, "}.", sep="")


def getChoice():
    # Ask if user would want to use a different weight bound
    print("\nWould you like to use a different weight bound? (y/n): ", end="")
    choice = input()
    while choice != 'y' and choice != 'n':
        print("\nInvalid choice, please enter 'y' or 'n': ", end="")
        choice = input()
    return choice


def main():
    if isfile("knapsack.txt"):

        # Open file
        print("\nThe file 'knapsack.txt' was found...")

        file = open("knapsack.txt", "r")
        line = file.readline().split()

        n = int(line[0])
        W = int(line[1])
        items = []

        # Read in items 
        print("\nReading in items...")
        for _ in range(n):
            line = file.readline().split()
            w = int(line[0])
            v = int(line[1])
            items.append(Item(w, v))
        
        # Close file
        file.close()

        # Compute table
        print("\nComputing solutions table...")
        table = computeTable(items, W)

        # Call function to print out optimal solution
        printOptimalSolution(table, items, W)
        
        # Ask if user would want to use a different weight bound
        choice = getChoice()

        while(choice == 'y'):
            # Ask user to enter a new weight bound
            print("\nEnter a new weight bound: ", end="")
            newWeight = int(input())

            while newWeight < 1 or newWeight > W:
                print("\nInvalid weight bound (must be between 1 and ", W, "), please enter a new weight bound: ", end="", sep="")
                newWeight = int(input())
            
            table = computeTable(items, newWeight)

            printOptimalSolution(table, items, newWeight)

            # Ask if user would want to use a different weight bound
            choice = getChoice()
            
        # End program
        print("\nProgram complete exiting...")
        return

    else: 
        # File not found, exit program
        print("\nknapsack.txt was not found, exiting...")
        return

# Run program
main()
