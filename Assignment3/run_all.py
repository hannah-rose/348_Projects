# -*- coding: utf-8 -*-
"""
Created on Saturday, May 2, 2015

@author: Hannah
"""

from hra069_kmg381_pbh423 import *

s="input_puzzles/easy/16_16.sudoku"

print"Backcheck Only"
b4=init_board(s)
solved_board = solve(b4,False,False,False,False)
print is_complete(solved_board)
print solved_board.count,"\n"

print "Forwardcheck Only"
b4=init_board(s)
solved_board = solve(b4,True,False,False,False)
print is_complete(solved_board)
print solved_board.count,"\n"
print 

print "FC with LCV"
print 
b4=init_board(s)
solved_board = solve(b4,True,False,False,True)
print is_complete(solved_board)
print solved_board.count,"\n"

print "FC with MRV"
b4=init_board(s)
solved_board = solve(b4,True,True,False,False)
print is_complete(solved_board)
print solved_board.count,"\n"

print "FC with MRV + LCV"
b4=init_board(s)
solved_board = solve(b4,True,True,False,True)
print is_complete(solved_board)
print solved_board.count,"\n"

print "FC with MCV"
b4=init_board(s)
solved_board = solve(b4,True,False,True,False)
print is_complete(solved_board)
print solved_board.count,"\n"

print "FC with MCV + LCV"
b4=init_board(s)
solved_board = solve(b4,True,False,True,True)
print is_complete(solved_board)
print solved_board.count,"\n"

#print is_complete(solved_board)
#print solved_board.count