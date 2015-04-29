# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 12:13:10 2015

@author: peter
"""

from SudokuStarter import *

verbose=0
b=init_board("input_puzzles/easy/9_9.sudoku")
b.print_board()
#test=getNextOpen(b)
backtrack(b)
#solved_board = solve(b)
b.print_board()
#solved_board.print_board()
print is_complete(b)