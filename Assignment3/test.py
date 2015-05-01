# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 12:13:10 2015

@author: peter
"""

from SudokuStarter import *

verbose=0

b=init_board("input_puzzles/more/more/9x9/9x9.3.sudoku")
b.print_board()
#test=getNextOpen(b)
#backtrack(b)
solved_board = solve(b,True,False,True,False)
#b.print_board()
solved_board.print_board()
print is_complete(solved_board)
print solved_board.count