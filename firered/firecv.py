#!/usr/bin/python

import retro
import time
import random
import sys
import world
    
# initialize game
env = retro.make('PokemonFireRedVersion-GbAdvance', 'Level1')
env.reset()

# proceeds clockwise
directions = [
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0], # move right
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], # move down
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], # move left
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]  # move up
]

actions = [
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0], # move right
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], # move down
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], # move left
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], # move up
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], # press A
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]  # press B
]

aButton = [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
bButton = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]

empty = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # empty action

tile = 16 # sixteen pixels in a square


def increment():
    for x in range(50):
        ob, rew, done, info = env.step(empty)
        env.render()
    return ob, rew, done, info
        
def waitForAnimation():
    for x in range(500):
        env.step(empty)
        env.render()
        
def allblack(ob):
    for i in range(160):
        for j in range(240):
            for k in range(3):
                if (ob[i][j][k]!=0):
                    return False
    return True

def inside(ob):
    for i in range(20, 218):
        if (ob[152][i][0]!=0 or ob[152][i][1]!=0 or ob[152][i][2]!=0):
            return False
    return True

def dialog(ob):
    for i in range(20, 218):
        if (ob[152][i][0]!=248 or ob[152][i][1]!=248 or ob[152][i][2]!=248):
            return False
    return True

def xy(info):
    return ((int)(info['x']/tile), (int)(info['y']/tile))

# getting started
ob, rew, done, info = increment()
x,y = xy(info)
world = world.World(x, y, 1)
world.printMap()

while True:
    # 5% chance that you press A, 10% chance B, 85% chance arrows
    '''
    buttonChoice = random.random()
    action = None
    if (buttonChoice < 0.05):
        action = aButton
    elif (buttonChoice < 0.15):
        action = bButton
    else:
        action = random.choice(directions)
    
    # take the action
    ob, rew, done, info = env.step(action)
    increment()
    '''
    
    # walk around world
    action = world.action()
    env.step(action)
    ob, rew, done, info = increment()
    x,y = xy(info)
    world.update(x, y)
    world.printMap()
    
    # detect traps
    '''
    if (allblack(ob)):
        print("black screen")
    elif (inside(ob)):
        print("leaving room")
        waitForAnimation()
        env.step(directions[1])
        increment()
    elif (dialog(ob)):
        print("talking to someone")
        waitForAnimation()
        env.step(aButton)
        increment()
    '''





















