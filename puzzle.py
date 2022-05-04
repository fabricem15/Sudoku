# Import sudoku module
import sudoku
# define main function
def main():
    '''
    The game is driven by the main function. Using the sudoku module, this program allows the user to play sudoku. 
    After providing the program with a file that contains the list of numbers in the game, the user is prompted to solve the puzzle
    by entering the location and value of the number they would like to insert in the format: row,col,num 
    '''

    file = input('Please enter your sudoku puzzle file: ' ) #Get file name
    print('Current grid')
    puzzle = sudoku.load_puzzle(file) #Read file and turn data into list of lists of integers.
    print(sudoku.puzzle_to_string(puzzle)) # Output the current grid

    numEntered = 0
    invalidNum = 0
    userInput = input('Enter move row/col/number (quit to exit):') # Ask user for information
    userInput = userInput.lower() #Make it case-insensitive
    
    while userInput != 'quit': #As long as the user doesn't quit game, keep asking for input
        
        data = userInput.split(',')
        # If the user enters a valid input, that is three numbers separated by a comma
        if len(data) == 3 and data[0].isdigit() and data[1].isdigit() and data[2].isdigit(): 
            row = int(data[0]) # row is the first number
            col = int(data[1]) # column is the second
            value = int(data[2]) # value to be inserted is third

            numEntered+=1
            # Check if each number is within range, otherwise input is invalid
            if 0 <= row < len(puzzle) and 0 <= col < len(puzzle) and 0<= value <= len(puzzle):
                oldNum = puzzle[row][col]# represents the number at the spot where the user is trying to input a new number.
                puzzle[row][col] = value #Add new value to the puzzle
                check1 = sudoku.check_rows(puzzle) #check rows
                check2 = sudoku.check_columns(puzzle)#check columns
                check3 = sudoku.check_subgrids(puzzle)#check subgrids
                
                #Check if any of the row/cols/subgrid is invalid
                # If any one of them is invalid, the input is invalid and the user is prompted to enter another value
                if len(check1) > 0 or len(check2) > 0 or len(check3) > 0: 
                    print('That is invalid.')
                    invalidNum +=1
                    puzzle[row][col] = oldNum # Return to the previous value if the user unsuccessfully tried to modify it
                # If the input is valid
                else: 
                    # The puzzle will only be complete when the user enters valid input that results in complete rows,columns, and subgrids
                    if sudoku.checkComplete(puzzle) == True:
                        print('The game has ended.')
                        print('\nPuzzle is complete!\n')
                        break # End the while loop and stop asking user for input
                    else: # Else if puzzle is yet to be completed, show user current grid with their new input
                        print('Current grid')
                        print(sudoku.puzzle_to_string(puzzle))
            else: # Else if number is out of range
                print('Invalid input.')
                invalidNum +=1
        else: # Else if the input doesn't match format
            print('Invalid input.')
        
        userInput = input('Enter move row/col/number (quit to exit):').lower()
    
    if sudoku.checkComplete(puzzle) == False: # if user quits the game
        print('The game has ended.\n\nPuzzle is NOT completed.\n')
    # When the game ends, output the following information
    if numEntered > 1:
        print(f'You entered {numEntered} numbers in total.')
    else:
        print(f'You entered {numEntered} number in total.')
    print(f'You entered {invalidNum} invalid numbers.')

#Main guard
if __name__ == "__main__":
    main()