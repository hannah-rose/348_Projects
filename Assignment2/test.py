# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 21:08:18 2015

@author: Peter
"""
from MancalaBoard import *

p1 = pbh423(1,Player.CUSTOM)
p2 = Player(2, Player.HUMAN)
mb = MancalaBoard()
mb.hostGame(p1, p2)