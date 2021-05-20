#!/usr/bin/python

import retro
import time
import random
import sys 

env = retro.make('PokemonEmeraldVersion-GbAdvance', 'Level1')
env.reset()
env.render()
    
empty = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # empty action

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

tile = 16 # sixteen pixels in a square

# initialize variables
xPos = 0
yPos = -tile
prevX = 0
prevY = -tile
deltaX = 0
deltaY = 0
info = None
direction = 1 # this is the index in the directions array

def update():
    global xPos, yPos, deltaX, deltaY
    prevX = xPos
    prevY = yPos
    xPos = info['xPos']
    yPos = info['yPos']
    deltaX = xPos-prevX
    deltaY = yPos-prevY
    #print("x = %d, y = %d" % (xPos, yPos))
    
def increment():
    global info
    for x in range(20):  # change this number for speed of play, lowest 20
        ob, rew, done, info = env.step(empty)
        env.render()
    
def step(direction):
    global info
    #print("going to move in direction %d" % direction)
    #print("x y before is %d %d" % (xPos/tile, yPos/tile))
    ob, rew, done, info = env.step(directions[direction])
    increment()
    update()
    #print("x y after is %d %d" % (xPos/tile, yPos/tile))
    #print("change x y is %d %d" % (deltaX/tile, deltaY/tile))

while True:
    step(direction)
    
    if (abs(deltaX) > tile and abs(deltaY) > tile):
        print("went through a door: deltaX is %d and deltaY is %d" % (deltaX/tile, deltaY/tile))
    elif (abs(deltaX) > tile or abs(deltaY) > tile):
        print("jumped: deltaX is %d and deltaY is %d" % (deltaX/tile, deltaY/tile))
    elif (deltaX==0 and deltaY==0):
        print("did not move, changing direction")
        direction = (direction + 1) % len(directions) #random.randint(len(directions))
        step(direction) # this one is to rotate
        step(direction) # this one is to move
        
        # check for stuck in corner
        if (deltaX==0 and deltaY==0):
            print("reached a corner, will turn back")
            direction = (direction + 1) % len(directions) #random.randint(len(directions))
            step(direction) # this one is to rotate
            step(direction) # this one is to move
            
            # check for dialog
            if (deltaX==0 and deltaY==0):
                print("could not turn back where I came from, will press A")
                ob, rew, done, info = env.step(aButton)
                increment()
                increment()
                increment()
                increment()
                # lol
    




















