#!/usr/bin/python

import retro
import time
import random
import sys
import gzip
import world
import sprite
import vision
    
# initialize game
env = retro.make(game='PokemonFireRedVersionV11-GbAdvance', state='lab', record='.')
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

RENDER_TO_SCREEN = True

# save game state to file
def saveState(env, name="test.state"):
    content = env.em.get_state()
    with gzip.open(name, 'wb') as f:
        f.write(content)

# the game takes several frames to respond to input, making this necessary
def increment():
    for _ in range(15): # 15 is the number of frames in a step
        ob, rew, done, info = env.step(empty)
        if RENDER_TO_SCREEN:
            env.render()
    return ob, rew, done, info

# the game takes several frames to respond to input, making this necessary
def incrementTransition():
    for _ in range(90): # 15 is the number of frames in a step
        ob, rew, done, info = env.step(empty)
        if RENDER_TO_SCREEN:
            env.render()
    return ob, rew, done, info

def incrementWalk():
    ob, rew, done, info = increment()

    # increment until character direction is observed
    i=15 # up to a maximum extra wait time of 15 frames
    while(s.characterDirection(ob) == -1 and i>0):
        ob, rew, done, info = env.step(empty)
        if RENDER_TO_SCREEN:
            env.render()
        i-=1

    return ob, rew, done, info

def xy(info):
    return ((int)(info['x']/tile), (int)(info['y']/tile))

def onTile(info):
    x = (int)(info['x'])
    y = (int)(info['y'])
    return x%tile==startX%tile and y%tile==startY%tile

# use world.py to walk around
def navigate(info):
    # update based on last move
    #x,y = xy(info)
    #world.update(x, y)
    #world.printMap()
    # ask world what to do
    action = world.action()
    # reset map if there's nothing to do
    if (action==empty):
        print("RESET MAP")
        world.reset()
        action = world.action()
    if (world.changingDirection):
        print("TURNING")
    else:
        print("WALKING")
    # perform action and SLAM
    env.step(action)

# getting started
ob, rew, done, info = increment()
startX = info['x']
startY = info['y']
x,y = xy(info)
world = world.World(x, y, 3) # starting direction is UP
world.printMap()
justMoved = False
justInteracted = False
lastAction = None

# sprite detector
s = sprite.Sprite()


# last save time
lastSave = time.time()

while True:
    # save state if enough time has elapsed
    seconds = time.time()
    if seconds - lastSave > 120:
        filename = f"test{int(seconds)}.state" 
        print("SAVING: " + filename)
        saveState(env, "states/"+filename)
        lastSave = seconds

    # wait to increment and respond to game
    #input("Press enter for next timestep")

    # increment the game
    ob, rew, done, info = incrementWalk()

    #print(s.characterDirection(ob))

    # update map from move
    if (justMoved and onTile(info)):
        justMoved = False
        x,y = xy(info)
        world.update(x, y)

    # determine what mode of the game we are in using vision
    if (vision.dialog(ob) or vision.pc(ob)):
        if lastAction!='interaction':
            print("INTERACTING")
        world.flagInteraction()
        if (vision.pc(ob)):
            print("EXIT PC")
            env.step(bButton)
        else:
            env.step(aButton)
        lastAction = 'interaction'
    elif (vision.battle(ob) or vision.attack(ob)):
        if lastAction!='battle':
            print("BATTLING")
        world.flagBattle()
        if (vision.battledialog(ob)):
            env.step(aButton)
        elif (vision.nopp(ob)):
            # try to find a move with PP
            env.step(random.choice(directions))
        else:
            env.step(aButton)
        lastAction = 'battle'
    elif (vision.allblack(ob)):
        if lastAction!='black':
            print("BLACK SCREEN")
        if (x==7 and y==0):
            print("black screen at 7,0 coordinates. will assume a warp")
            world.warp()
        ob, rew, done, info = incrementTransition()
        #env.step(empty)
        lastAction = 'black'
    else:
        # walk around world
        if (onTile(info)):
            navigate(info)
            justMoved = True
        else:
            print('WAITING FOR STEP')
            print(info['x'])
            print(info['y'])
            env.step(empty)
        # show newest understanding of the world
        # as of the last move and plans for next move
        world.printMap()
        lastAction = 'move'

    '''
    if (vision.inside(ob)):
        print("leaving room")
        #world.reset()
        #waitForAnimation()
        #env.step(directions[1])
        #increment()
    '''
