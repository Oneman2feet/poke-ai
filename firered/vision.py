#!/usr/bin/python

import sys

black = [0, 0, 0]
white = [248, 248, 248]
blue = [40, 80, 104]
grey = [112, 104, 128]
red = [232, 0, 0]

def sameColor(a, b):
    return a[0]==b[0] and a[1]==b[1] and a[2]==b[2]
        
def allblack(ob):
    for i in range(160):
        for j in range(240):
            for k in range(3):
                if (not sameColor(ob[i][j], black)):
                    return False
    return True

def inside(ob):
    for i in range(20, 218):
        if (not sameColor(ob[152][i], black)):
            return False
    return True

def dialog(ob):
    for i in range(20, 218):
        if (not sameColor(ob[152][i], white)):
            return False
    return True

def battle(ob):
    for i in range(11, 114):
        if (not sameColor(ob[121][i], blue)):
            return False
    return True

def battledialog(ob):
    for i in range(11, 218):
        if (not sameColor(ob[121][i], blue)):
            return False
    return True

def attack(ob):
    for i in range(9, 151):
        if (not sameColor(ob[116][i], grey)):
            return False
    return True

def pc(ob):
    for i in range(15, 109):
        if (not sameColor(ob[4][i], grey)):
            return False
    return True

def nopp(ob):
    for i in range(127, 132):
        if (not sameColor(ob[i][168], red)):
            return False
    return True
