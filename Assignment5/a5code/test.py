# -*- coding: utf-8 -*-
"""
Created on Thu Jun 04 22:26:09 2015

@author: Peter
"""
execfile("StrokeHmm.py")
#x = StrokeLabeler()
#x.trainHMMDir("../trainingFiles/") #../ means go back a directory
x.labelFile("../trainingFiles/0128_1.6.1.labeled.xml", "results.txt")