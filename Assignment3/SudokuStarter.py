#!/usr/bin/env python
import struct, string, math


verbose=0

class SudokuBoard:
    """This will be the sudoku board game object your player will manipulate."""
  
    def __init__(self, size, board, domain):
      """the constructor for the SudokuBoard"""
      self.BoardSize = size #the size of the board
      self.CurrentGameBoard= board #the current state of the game board
      self.Domain = domain #the set of possible values for each cell


    def set_value(self, row, col, value):
        """This function will create a new sudoku board object with the input
        value placed on the GameBoard row and col are both zero-indexed"""

        #add the value to the appropriate position on the board
        self.CurrentGameBoard[row][col]=value
        #return a new board of the same size with the value added
        return SudokuBoard(self.BoardSize, self.CurrentGameBoard, self.Domain)
                                                                  
                                                                  
    def print_board(self):
        """Prints the current game board. Leaves unassigned spots blank."""
        div = int(math.sqrt(self.BoardSize))
        dash = ""
        space = ""
        line = "+"
        sep = "|"
        for i in range(div):
            dash += "----"
            space += "    "
        for i in range(div):
            line += dash + "+"
            sep += space + "|"
        for i in range(-1, self.BoardSize):
            if i != -1:
                print "|",
                for j in range(self.BoardSize):
                    if self.CurrentGameBoard[i][j] > 9:
                        print self.CurrentGameBoard[i][j],
                    elif self.CurrentGameBoard[i][j] > 0:
                        print "", self.CurrentGameBoard[i][j],
                    else:
                        print "  ",
                    if (j+1 != self.BoardSize):
                        if ((j+1)//div != j/div):
                            print "|",
                        else:
                            print "",
                    else:
                        print "|"
            if ((i+1)//div != i/div):
                print line
            else:
                print sep


def parse_file(filename):
    """Parses a sudoku text file into a BoardSize, and a 2d array which holds
    the value of each cell. Array elements holding a 0 are considered to be
    empty."""

    f = open(filename, 'r')
    BoardSize = int( f.readline())
    NumVals = int(f.readline())

    #initialize a blank board
    board= [ [ 0 for i in range(BoardSize) ] for j in range(BoardSize) ]

    #populate the board with initial values
    for i in range(NumVals):
        line = f.readline()
        chars = line.split()
        row = int(chars[0])
        col = int(chars[1])
        val = int(chars[2])
        board[row-1][col-1]=val
    
    return board
    

def is_complete(sudoku_board):
    """Takes in a sudoku board and tests to see if it has been filled in
    correctly."""
    BoardArray = sudoku_board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))

    #check each cell on the board for a 0, or if the value of the cell
    #is present elsewhere within the same row, column, or square
    for row in range(size):
        for col in range(size):
            if BoardArray[row][col]==0:
                return False
            for i in range(size):
                if ((BoardArray[row][i] == BoardArray[row][col]) and i != col):
                    return False
                if ((BoardArray[i][col] == BoardArray[row][col]) and i != row):
                    return False
            #determine which square the cell is in
            SquareRow = row // subsquare
            SquareCol = col // subsquare
            for i in range(subsquare):
                for j in range(subsquare):
                    if((BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j]
                            == BoardArray[row][col])
                        and (SquareRow*subsquare + i != row)
                        and (SquareCol*subsquare + j != col)):
                            return False
    return True


def init_board(file_name):
    """Creates a SudokuBoard object initialized with values from a text file"""
    board = parse_file(file_name)
    domain = create_domain(board,len(board))
    return SudokuBoard(len(board), board, domain)


def create_domain(board,size):
    """Initializes domain of all possibilities for each cell
       Called from init_board"""
    #Initialize blank domain
    domain = [ [ 0 for i in range(size) ] for j in range(size) ]
    #Fill in with every possible option
    for row in range(size):
        for col in range(size):
            domain[row][col] = list(range(1,size+1))
    return domain


def init_domain(board,size):
    """Uses forward checking to remove conflicts from initial puzzle.
       Must be called after init_board to work correctly"""
    domain = board.Domain
    BoardArray = board.CurrentGameBoard
    #Update conflicts based on items already in the sudoku
    for row in range(size):
        for col in range(size):
            if (BoardArray[row][col])!=0:
                domain[row][col] = [ BoardArray[row][col] ]
                forwardcheck(board,domain,row,col)
    return domain



def solve(initial_board, forward_checking = False, MRV = False, MCV = False,
    LCV = False):
    """Takes an initial SudokuBoard and solves it using back tracking, and zero
       or more of the heuristics and constraint propagation methods (determined by
       arguments). Returns the resulting board solution. """
    #Begin by initializing the domain
    init_domain(initial_board,initial_board.BoardSize)

    print "Be patient! We're working on solving your puzzle..."

    #Call backtrack with the required constraints
    if forward_checking:
        back_forward(initial_board, initial_board.Domain)
    else:
        backtrack(initial_board)
    return initial_board


def backtrack(board):
    """Recursive implementation to solve a Sudoku board. Uses brute force to
    check all possible solutions. If it cannot find one, it backtracks and undos
    one of its guesses and continues."""
    
    arr=getNextOpen(board)    
    row=arr[0]
    col=arr[1]
    if verbose==1:
        print "next open spot is %d, %d" % (row,col) 
    if (row==-1):
        #no Open Spots were found. All spots are filled so we are done
        return True
    
    BoardArray = board.CurrentGameBoard
    size = len(BoardArray)
    
    #we will check if any of these values work
    for test in range (1, size+1):
        #check if this test is a valid move.
        if(noConflictCheck(board,test,row,col)):
            if verbose==1:
                print "No conflict setting value. New Board:"
            #Set new value
            board.set_value(row,col,test)
            #if we are done, pass the true back through the recursion
            if (backtrack(board)):
                return True
            #else undo the move and keep trying
            board.set_value(row,col,0)     
    #if nothing else is found go back and change the most recent value
    return False


def back_forward(board, domain):
    """Recursive implementation to solve a Sudoku board. Implements
       forward checking into backtracking algorithm"""
    
    arr=getNextOpen(board)    
    row=arr[0]
    col=arr[1]
    if (row==-1):
        #no Open Spots were found. All spots are filled so we are done
        return True
    
    BoardArray = board.CurrentGameBoard
    size = len(BoardArray)
    
    #Check each open value
    for test in range (1, size+1):
        #check if this test is a valid move.
        if(noConflictCheck(board,test,row,col)):
            #Set new value
            domain_test = domain
            board.set_value(row,col,test)
            #Assess its domain and check for empty domains
            if forwardcheck(board, domain_test, row, col):
                if back_forward(board, domain_test):
                    return True
            #else undo the move and keep trying
            board.set_value(row,col,0)         
    #if nothing else is found go back and change the most recent value
    return False


def forwardcheck(board, domain, row, col):
    """After each new value is assigned, delete all conflicting values from other squares' domains"""
    #Remove new value from conflicting squares
    BoardArray = board.CurrentGameBoard
    val = BoardArray[row][col]
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))
    
    #Check rows and columns for conflicts
    for i in range(size):
        if ((domain[row][i].count(val)!=0) and i != col):
            (domain[row][i]).remove(val)
        if ((domain[i][col].count(val)!=0) and i != row):
            (domain[i][col]).remove(val)

    #determine which square the cell is in and remove conflicts
    SquareRow = row // subsquare
    SquareCol = col // subsquare
    for i in range(subsquare):
        for j in range(subsquare):
            if((domain[SquareRow*subsquare+i][SquareCol*subsquare+j]).count(val)!=0
                and (SquareRow*subsquare + i != row)
                and (SquareCol*subsquare + j != col)):
                    (domain[SquareRow*subsquare+i][SquareCol*subsquare+j]).remove(val)

    #Check for empty domains
    if domain.count([])!=0:
        return False
    return True                



def getNextOpen(board):
    """Returns the next empty spot, which is shown as a 0 in our array
    If it can't find one, it returns [-1,-1], which means the puzzle is complet
    Otherwise it returns an array formatted [row, col]"""
    for i in range (0,board.BoardSize):
        for j in range (0,board.BoardSize):
            if board.CurrentGameBoard[i][j]==0:
                #return the row and col 
                return [i,j]
    #else return false, so we are done
    return [-1,-1]
    

def noConflictCheck(board,num,row,col):
    """Shortened version of is_complete. Only checks the row, col and subsquare
    that we are checking. """
    BoardArray = board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))
    
    for i in range(size):
        if ((BoardArray[row][i] == num) and i != col):
            return False
        if ((BoardArray[i][col] == num) and i != row):
            return False
    #determine which square the cell is in
    SquareRow = row // subsquare
    SquareCol = col // subsquare
    for i in range(subsquare):
        for j in range(subsquare):
            if((BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j] == num)
                and (SquareRow*subsquare + i != row)
                and (SquareCol*subsquare + j != col)):
                    return False
    return True