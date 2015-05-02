# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 12:13:10 2015

@author: peter
"""

from hra069_kmg381_pbh423 import *

verbose=0

b=init_board("input_puzzles/easy/9_9.sudoku")
#b=init_board("input_puzzles/more/more/16x16/16x16.3.sudoku")
b.print_board()
#test=getNextOpen(b)
#backtrack(b)
solved_board = solve(b,True,False,True,False)
#b.print_board()
solved_board.print_board()
print is_complete(solved_board)
print solved_board.count