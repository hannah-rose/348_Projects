# -*- coding: utf-8 -*-
"""
Created on Thu Jun 04 22:26:09 2015

@author: Peter
"""
# Train and test best
execfile("StrokeHmm.py")
sl = StrokeLabeler()
sl.trainHMMDir("../trainingFiles/")
labels,myLabels=sl.testBatch("../trainingFiles/")
print len(labels)
print len(myLabels)
best_returns=sl.confusion(labels,myLabels)

# Train and test basic
execfile("StrokeHmmbasic.py")
sl = StrokeLabeler()
sl.trainHMMDir("../trainingFiles/")
labels,myLabels=sl.testBatch("../trainingFiles/")
print len(labels)
print len(myLabels)
basic_returns=sl.confusion(labels,myLabels)

# Print results
print "Best: "+str(best_returns)
print "Basic: "+str(basic_returns)
