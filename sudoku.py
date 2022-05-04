
import math
#------------------------------------------------------------------#
def load_puzzle(filename):
    ''' Reads a sudoku puzzle from the text file 'filename' in the current directory. 
        Returns a list of lists of integers that represents the game.
            load_puzzle(filename:str) -> str[str[int]]
        Empty cells in the game are denoted by 0s in the file (and the output list)
    '''
    puzzle = []
    
    with open(filename, "r") as f:
        for line in f:
            puzzle.append( [int(val) for val in line.split(",")] )

    return puzzle


#------------------------------------------------------------------#
#------------------------------------------------------------------#


# your functions go here!


def puzzle_to_string(puzzle) -> str:
    '''
    Outputs a visual representation of the sudoku game in the row-column-subgrid format.
        Let n represent the number of elements in the provided list.
        Numbers are separated by a space character and  '|' is added after √n numbers in a row.
        Dashes are added after √n number of rows underneath the numbers to separate them into subgrids.
    
    Pre-condition: puzzle must be a list of lists of integers.

    Post-conditon: returns the visual representation of the list of lists with numbers nicely aligned.   
    '''

    sudoku = '' # final output
    n = int(math.sqrt(len(puzzle)))

    colSeparator = 0
    rowSeparator = 0

    #There are n indexes in the list maxSubgrid that represents the maximum number of space required for each number.
    # Each index also determines the amount of '-' each subgrid that goes below each subgrid
    maxSubgrid = [0]*n 
    biggestNum = 0
    
    for i in range(len(puzzle)):
        maxNumLength = 0 
        counter = 0
        index = 0
    
    # Algorithm for determining the amount of space to allocate for each number
        for k in range(len(puzzle)): # Go through each list in the puzzle
            if puzzle[i][k] > biggestNum: #Determine the largest number in the list, whose length determines the max amount of space required for each number
                biggestNum = puzzle[i][k]
            if counter < n: #Check every n digits
                maxNumLength += len(str(puzzle[i][k])) #append the length of the current number to the size of the subrow(n digits)
                counter+=1
            elif counter == n: #Reset the counter
                if maxNumLength > maxSubgrid[index]:
                    maxSubgrid[index] = maxNumLength
                
                index+=1 #Increase index of subgrid
                maxNumLength = 0
                counter = 1 # Count is reset to 1
                maxNumLength += len(str(puzzle[i][k]))
       
        if maxNumLength > maxSubgrid[index]: #Set the maximum space required 
            maxSubgrid[index] = maxNumLength
     
    spaceGiven = len(str(biggestNum)) + 1 #Space allocated for the largest number and consequently to all numbers in the puzzle for uniformity. 

    for i in range(len(puzzle)): # Go through the list of lists
        colSeparator = 0
        if rowSeparator == n: # Separate after n rows
            for l in range(len(maxSubgrid)):
                if 0 < l < len(maxSubgrid)-1: #If it's a subgrid that's not at the extremities, add an extra dash
                        sudoku += '-' * (spaceGiven * n +1)
                else:
                    sudoku += '-' * (spaceGiven * n) # Add (n*2) dashes as the row separators
                if l != len(maxSubgrid)-1:
                    sudoku += '+' #Add plus sign in between subgrids
     
            sudoku += '\n'
            rowSeparator = 0 #reset row separator
        
        for k in range(len(puzzle[0])): # Go through the length of each row to add the numbers and column separators 
            if colSeparator == n: # Separate after n columns
                sudoku += '| '
                colSeparator = 0
            # Add each number with f-strings formatting.
            # Each number is left-justified depending on the length of the biggest number in the list.
            if puzzle[i][k] != 0:
                sudoku += f"{puzzle[i][k]:<{spaceGiven}}" 
            else:
                sudoku += f"{' ':<{spaceGiven}}"
            colSeparator += 1
        
        sudoku += '\n'
        rowSeparator += 1 #Increase row separator after each row

    return sudoku

def check_rows(puzzle)-> list:
    '''
    Checks if each row in the given list of lists is valid.

    A row is valid if:
        - There are no repetition of numbers.
        - It only consists of 0s.
        - Every digit in the row is ≥ 0 and ≤ the length of the list puzzle.
    
    Returns an empty list if valid. Otherwise returns the row number(s) that is/are invalid.
    '''
    valid = []
    for i in range(len(puzzle)):
        if ValidDigit(puzzle[i]) == False: # First check if all digits are valid
            valid.append(i)
        elif ValidDigit(puzzle[i]) == True: #If all digits are within range: len(puzzle)
            if checkRepeats(puzzle[i]) == True: # Check for repetitions
                valid.append(i)
    return valid

def check_columns(puzzle)->list:
    '''
    Checks if each column in the given list of lists is valid.

    A column is valid if:
        - There are no repetition of numbers.
        - It only consists of 0s.
        - Every digit in the column is ≥ 0 and ≤ the length of the list puzzle.
    Returns an empty list if valid. Otherwise returns the column number(s) that is/are invalid.

    '''
    invalid = []
    listOfColumns = []
    # Get each indivual column from the puzzle
    for col in range(len(puzzle)):
        column = []
        for row in range(len(puzzle)):
            column.append(puzzle[row][col])
        listOfColumns.append(column) 

    for i in range(len(listOfColumns)):
        if ValidDigit(listOfColumns[i]) == False: # First check if all digits are valid
            invalid.append(i)
        elif ValidDigit(listOfColumns[i]) == True: #If all digits are within range: len(puzzle)
            if checkRepeats(listOfColumns[i]) == True: # Check for repetitions
                invalid.append(i)
        
    return invalid

def check_subgrids(puzzle: list)->list:
    '''
    Checks if each subgrid in the given list of lists is valid.

    A subgrid is valid if:
        - There are no repetition of numbers(0s excluded).
        - It only consists of 0s.
        - Every digit in the subgrid is ≥ 0 and ≤ the length of the list puzzle.
    
    Parameter: puzzle-> list[list[int]]

    Returns an empty list if valid. Otherwise returns the subgrid number(s) that is/are invalid.
    '''

    valid = []
    subgrids = getSubgrids(puzzle) #Get subgrids from helper function
    for i in range(len(subgrids)):
        if ValidDigit(subgrids[i]) == False:# First check if all digits are valid
            valid.append(i)
        elif ValidDigit(subgrids[i]) == True:
            if checkRepeats(subgrids[i]) == True: # Then check for repetitions
                valid.append(i)

    return valid

#-------------------#
# Helper functions below #
#-------------------#

def checkComplete(puzzle:list)->bool:
    '''
    Checks if the puzzle is complete. That is, every row and column is filled with numbers other than 0. 
    It does not check for repeating values because that is performed by another helper function.
    '''
    complete = True
    # Only need to check every row and column
    # Because subgrids are made of rows and columns
    for i in range(len(puzzle)):
        for k in range(len(puzzle)):
            if puzzle[i][k] == 0:
                complete = False
                break
    return complete

def checkRepeats(myList:list)-> bool:
    '''
    Checks the occurrences of each number (x | x > 0) in the provided list. If the number occurs more than once, the list is invalid.
    
    Parameters: myList = 1D list of int.

    Post-condition: returns False if every number(except 0) in the list occurs exactly once. Otherwise, returns True.
    '''
    repetition = [0] * len(myList) # each number refers to the frequency of index+1 in the list
    repeats = False

    for i in range(len(myList)):
        index = myList[i] - 1
        if myList[i] != 0: #Ignore 0s
            repetition[index] += 1 # increase frequency of that number by 1

            if repetition[index] > 1: #If a number occurs more than once 
                repeats = True # return that there are multiple repeats of a number in the list
                break 
            
    return repeats

def ValidDigit(myList:list)-> bool:
    '''
    Checks if every number in the list is within range(0, length of myList).

    Parameter(s): myList = 1D list of int.

    Post-condition: returns True if every number x is 0 <= x <= len(myList). Otherwise, return False.
    '''

    valid = True
    for i in range(len(myList)):
        if not myList[i] in range(len(myList)+1): # Check if each number in the list is valid
            valid = False
            break
    return valid

def getSubgrids(puzzle: list)->list:
    '''
    Retrieves individual subgrids from the list of lists of int and returns a list of lists of subgrids.

    Parameters: puzzle = list of lists of int.

    Post-condition: returns a list of lists of integers. Each list of integers represents a subgrid in the puzzle.
    '''
    counter = 0
    index = 0

    n = math.sqrt(len(puzzle)) # Represents the number of rows and columns per subgrid.
    m = len(puzzle)

    listOfSubgrids = []
    for i in range(m):
        listOfSubgrids.append([]) # Fill my list with empty lists

   
    for i in range(m):
        counter = 0 #Reset counter

        if i % n == 0: # Allows us to change subgrids after n numbers
            index = i
            section = i # Record the new anchor point
        
        # This statement allows us to go back to a previous or new anchor point when a new row starts
        # For instance, when row 3 starts in a 9x9 sudoku puzzle, the anchor point is now 3(previous was 0)
        #   So, when row 4 starts, the subgrid index is reset to the anchor point since 4 / 3 != 0
        # This is what helps the function resume to the anchor subgrid index  
        else: 
            index = section
        
        for k in range(m): # Go through each number in the row
            # Add n numbers at a time to each subgrid
            if counter < n: 
                listOfSubgrids[index].append(puzzle[i][k])# Add that numnber to a new subgrid
                counter += 1 #increase counter

            elif counter == n: 
                index+=1 # Change subgrid index
                listOfSubgrids[index].append(puzzle[i][k]) # Add that numnber to a new subgrid
                counter = 1 # Reset counter to 1 and not 0 because a number has been added 
    return listOfSubgrids

def main():
    puzzle = load_puzzle('puzzle1.csv')
    # print(puzzle)
    print(puzzle_to_string(puzzle))
    # print(checkComplete(puzzle))
    # print(check_rows(puzzle))
    # print(check_columns(puzzle))
    # print(check_subgrids(puzzle))
    
    
# Guard for main function - do NOT remove or change
if __name__ == "__main__":
    main()
