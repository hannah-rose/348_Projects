# -*- coding: utf-8 -*-
"""
Created on Tue May 12 16:04:49 2015

@author: peter
"""
from bayes_template import *

b=Bayes_Classifier(0)
b.validate()
temp=b.tokenize("test 1 2 . ? the ",1)
print b.classify("good awsome amazing")
print b.classify("bad horrible aweful")
print b.classify("the movie was ok")