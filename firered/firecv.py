#!/usr/bin/python

import retro
import time
import random
import sys
import world
import vision
    
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
    for x in range(2000):
        env.step(empty)
        env.render()

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
    if (action==empty):
        world.reset()
        action = world.action()
    
    # SLAM
    env.step(action)
    ob, rew, done, info = increment()
    x,y = xy(info)
    world.update(x, y)
    world.printMap()
    
    while (vision.dialog(ob)):
        world.flagInteraction()
        env.step(aButton)
        ob, rew, done, info = increment()
    
    while (vision.battle(ob) or vision.attack(ob)):
        if (vision.battledialog(ob)):
            env.step(aButton)
            ob, rew, done, info = increment()
        else:
            env.step(aButton)
            waitForAnimation()
            ob, rew, done, info = increment()
    
    # detect traps
    if (vision.allblack(ob)):
        print("black screen")
    elif (vision.inside(ob)):
        print("leaving room")
        #world.reset()
        #waitForAnimation()
        #env.step(directions[1])
        #increment()





















