# -*- coding: utf-8 -*-
"""
Created on Thu Jun 04 22:26:09 2015

@author: Peter
"""
execfile("StrokeHmm.py")
sl = StrokeLabeler()
sl.trainHMMDir("../trainingFiles/")
labels,myLabels=sl.testBatch("../trainingFiles/")
print len(labels)
print len(myLabels)
returns=sl.confusion(labels,myLabels)
print returns