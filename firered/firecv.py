#!/usr/bin/python

import retro
import time
import random
import sys
import world
import vision
    
# initialize game
env = retro.make('PokemonFireRedVersion-GbAdvance', 'start')
env.reset()

directions = [
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0], # move right
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], # move down
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], # move left
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]  # move up
]

aButton = [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
bButton = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

empty = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # empty action

tile = 16 # sixteen pixels in a square


def increment():
    for _ in range(30):
        ob, rew, done, info = env.step(empty)
        env.render()
    return ob, rew, done, info
        
def waitForAnimation():
    for _ in range(2000):
        env.step(empty)
        env.render()

def xy(info):
    return ((int)(info['x']/tile), (int)(info['y']/tile))

def onTile(info):
    x = (int)(info['x'])
    y = (int)(info['y'])
    return x%tile==startX%tile and y%tile==startY%tile

# use world.py to walk around
def navigate(info):
    # update based on last move
    x,y = xy(info)
    world.update(x, y)
    world.printMap()
    # ask world what to do
    action = world.action()
    # reset map if there's nothing to do
    if (action==empty):
        world.reset()
        action = world.action()
    # perform action and SLAM
    env.step(action)

# getting started
ob, rew, done, info = increment()
startX = info['x']
startY = info['y']
x,y = xy(info)
world = world.World(x, y, 1)
world.printMap()

while True:
    # increment the game
    ob, rew, done, info = increment()

    # determine what mode of the game we are in using vision
    if (vision.dialog(ob) or vision.pc(ob)):
        print("IN DIALOG / PC")
        world.flagInteraction()
        if (vision.pc(ob)):
            env.step(bButton)
        else:
            env.step(aButton)
    elif (vision.battle(ob) or vision.attack(ob)):
        print("IN BATTLE")
        world.flagBattle()
        if (vision.battledialog(ob)):
            env.step(aButton)
        elif (vision.nopp(ob)):
            # try to find a move with PP
            env.step(random.choice(directions))
        else:
            env.step(aButton)
    elif (vision.allblack(ob)):
        print("IN BLACK SCREEN")
        env.step(empty)
    else:
        print("WALKING")
        # walk around world
        if (onTile(info)):
            navigate(info)
        else:
            print('not on tile')
            print(info['x'])
            print(info['y'])
            env.step(empty)
    
    '''
    if (vision.inside(ob)):
        print("leaving room")
        #world.reset()
        #waitForAnimation()
        #env.step(directions[1])
        #increment()
    '''
