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

aButton = [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
bButton = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

empty = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # empty action

tile = 16 # sixteen pixels in a square


def increment():
    for x in range(20):
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
        if (vision.pc(ob)):
            env.step(bButton)
        else:
            env.step(aButton)
        ob, rew, done, info = increment()
    
    while (vision.battle(ob) or vision.attack(ob)):
        if (vision.battledialog(ob)):
            env.step(aButton)
            ob, rew, done, info = increment()
        else:
            env.step(aButton)
            #waitForAnimation()
            ob, rew, done, info = increment()
    
    # detect traps
    while (vision.allblack(ob)):
        print("black screen")
        x = info['x']
        y = info['y']
        print((x, y))
        ob, rew, done, info = increment()
        print((info['x'], info['y']))
        if (info['x']!=x or info['y']!=y):
            world.reset() # warped
    if (vision.inside(ob)):
        print("leaving room")
        #world.reset()
        #waitForAnimation()
        #env.step(directions[1])
        #increment()
