#!/usr/bin/python

import time
import random
import operator

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

# proceeds clockwise
directions = [
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0], # move right
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], # move down
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], # move left
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]  # move up
]

# do nothing
empty = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# A button
aButton = [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]

# ASCII tiles for map
unknown = '/'
start = 'X'
door = 'D'
player = '*'
wall = '#'
ground = '.'
interactable = '@'
goal = 'G'
impossible = '?'
frontier = 'F'

class World:     

    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.prevX = x
        self.prevY = y
        self.direction = direction
        self.mapOfMaps = []
        self.reset()
        
    def reset(self, warp=False):
        self.changingDirection = False
        self.shouldInteract = False
        self.justBattled = False
        self.origin = [1, 1]
        self.map = [[unknown, unknown, unknown], [unknown, start, unknown], [unknown, unknown, unknown]]
        self.goal = None
        self.playerRow = 0
        self.playerCol = 0

        if warp:
            # mark door as behind you
            negDoorDirection = self.directionDelta(self.direction)
            self.map[1 - negDoorDirection[0]][1 - negDoorDirection[1]] = door

            # populate frontier with other three directions
            self.frontier = [ self.directionDelta((self.direction + i) % 4) for i in range(1, 4) ]
        else:
            self.frontier = [ self.directionDelta((self.direction + i) % 4) for i in range(4) ]

        print(self.frontier)

    def warp(self):
        # add to map of maps if not trivial in size
        if (len(self.map) > 3 or len(self.map[0]) > 3):
            self.mapOfMaps.append(self.map)
        # start map of new area
        self.reset(warp=True)
        self.printMapOfMaps()
        
    # most coordinates are with respect to the player starting position as 0,0
    # first coordinate is always the row and second the column
    # to convert this to the map coordinates, we translate by the location of the player start (origin)
    def toMap(self, rowCol):
        return (rowCol[0]+self.origin[0], rowCol[1]+self.origin[1])
    def fromMap(self, rowCol):
        return (rowCol[0]-self.origin[0], rowCol[1]-self.origin[1])

    def printMap(self, map=None):
        if map==None:
            map = self.map
        for row in map:
            print("\n", end =" "),
            for entry in row: 
                print(entry, end = " "),
        print("\n")

    def printMapOfMaps(self):
        print("MAP OF MAPS:")
        for map in self.mapOfMaps:
            self.printMap(map=map)
            print("-----------")
        print("END MAP OF MAPS")
        
    def printMatrix(self, matrix):
        for row in matrix:
            print("\n", end =" "),
            for entry in row:
                print(entry, end = " "),
        print("\n")

    def cost(self, item):
        if (item==unknown or item==goal or item==frontier):
            return 1
        elif (item==ground or item==player):
            return 1
        elif (item==wall or item==interactable or item==start or item==door):
            return 0
        else:
            return -1
        
    # return array of directions needed to move to the goal
    # NOTE: uses col row order instead of row col!
    def pathfind(self):
        # convert map to cost matrix
        matrix = [ [ self.cost(item) for item in row ] for row in self.map ]
        #self.printMatrix(matrix)
        # input to pathfinding algorithm
        grid = Grid(matrix=matrix)
        # determine start and end
        startRow, startCol = self.toMap((self.playerRow, self.playerCol))
        endRow, endCol = self.toMap(self.goal)
        start = grid.node(startCol, startRow)
        end = grid.node(endCol, endRow)
        finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
        path, runs = finder.find_path(start, end, grid)
        return path

    def directionTo(self, position):
        rowDiff, colDiff = tuple(map(operator.sub, position, self.toMap((self.playerRow, self.playerCol))))
        if (rowDiff==0 and colDiff==1):
            return 0
        elif (rowDiff==1 and colDiff==0):
            return 1
        elif (rowDiff==0 and colDiff==-1):
            return 2
        elif (rowDiff==-1 and colDiff==0):
            return 3
        else:
            return None

    def isGoal(self, row, col):
        if self.goal==None:
            return False
        return row==self.goal[0] and col==self.goal[1]

    def action(self):
        # press A if we just hit something
        if (self.shouldInteract):
            #print("interact with tile")
            return aButton
        # choose where to go based on the map
        while (self.goal==None or (self.isGoal(self.playerRow, self.playerCol))):
            # check for traps
            if (len(self.frontier)==0):
                return empty
            # grab from the frontier
            self.goal = self.frontier.pop()
        # pathfind to goal
        path = self.pathfind()
        while (len(path)<2):
            # mark impossible goal on map
            goalRow, goalCol = self.toMap(self.goal)
            if (self.map[goalRow][goalCol]!=start and self.map[goalRow][goalCol]!=door):
                self.map[goalRow][goalCol] = impossible
            # check for traps
            if (len(self.frontier)==0):
                return empty
            # grab from the frontier
            self.goal = self.frontier.pop()
            path = self.pathfind()
        # show goal on map
        print(self.goal)
        goalRow, goalCol = self.toMap(self.goal)
        self.map[goalRow][goalCol] = goal
        # get next step
        (c,r) = path.pop(1)
        # determine direction to next step
        newDirection = self.directionTo((r,c))
        # flag changingDirection if so
        if (newDirection!=self.direction):
            self.changingDirection = True
            self.direction = newDirection
        return directions[self.direction]

    # convert direction to row,col deltas
    def directionDelta(self, direction):
        if (direction==-1):
            return (0, 0)
        elif (direction==0):
            return (0, 1)
        elif (direction==1):
            return (1, 0)
        elif (direction==2):
            return (0, -1)
        elif (direction==3):
            return (-1, 0)
        else:
            return None
    
    def addFrontier(self, row, col):
        mapRow, mapCol = self.toMap((row, col))
        tile = self.map[mapRow][mapCol]
        if (tile==unknown and not (row, col) in self.frontier):
            self.frontier.append((row, col))
            self.map[mapRow][mapCol] = frontier
        
    def removeFrontier(self, row, col):
        if ((row, col) in self.frontier):
            self.frontier.remove((row, col))
        # remove goal if it is impossible
        if (self.goal!=None and self.goal[0]==row and self.goal[1]==col):
            self.goal = None
    
    def expandMap(self, direction):
        # convert to map coordinates
        mapPlayerRow, mapPlayerCol = self.toMap((self.playerRow, self.playerCol))
        if (self.direction==0):
            if (mapPlayerCol==len(self.map[0])-1):
                # add element at end of each row
                for row in self.map:
                    row.append(unknown)
                # player position does not change
            # add up, right, down to frontier if not already visited
            self.addFrontier(self.playerRow-1, self.playerCol)
            self.addFrontier(self.playerRow+1, self.playerCol)
            self.addFrontier(self.playerRow, self.playerCol+1) # current direction added last
        elif (self.direction==1):
            if (mapPlayerRow==len(self.map)-1):
                # add new row at end
                self.map.append([unknown]*len(self.map[0]))
                # player position does not change
            # add left, down, right to frontier if not already visited
            self.addFrontier(self.playerRow, self.playerCol-1)
            self.addFrontier(self.playerRow, self.playerCol+1)
            self.addFrontier(self.playerRow+1, self.playerCol) # current direction added last
        elif (self.direction==2):
            if (mapPlayerCol==0):
                # add element at start of each row
                for row in self.map:
                    row.insert(0, unknown)
                # shift map origin column by one
                self.origin[1] += 1
            # add up, left, down to frontier if not already visited
            self.addFrontier(self.playerRow-1, self.playerCol)
            self.addFrontier(self.playerRow+1, self.playerCol)
            self.addFrontier(self.playerRow, self.playerCol-1) # current direction added last
        elif (self.direction==3):
            if (mapPlayerRow==0):
                # add new row at beginning
                self.map.insert(0, [unknown]*len(self.map[0]))
                # shift map origin row by one
                self.origin[0] += 1
            # add left, up, right to frontier if not already visited
            self.addFrontier(self.playerRow, self.playerCol-1)
            self.addFrontier(self.playerRow, self.playerCol+1)
            self.addFrontier(self.playerRow-1, self.playerCol) # current direction added last
        else:
            # default behavior is to try expanding in all directions
            self.expandMap(0)
            self.expandMap(1)
            self.expandMap(2)
            self.expandMap(3)

    def flagInteraction(self):
        deltaRow, deltaCol = self.directionDelta(self.direction)
        pRow, pCol = self.playerRow + deltaRow, self.playerCol + deltaCol
        mapRow, mapCol = self.toMap((pRow, pCol))
        if (self.map[mapRow][mapCol]!=start and self.map[mapRow][mapCol]!=door):
            self.map[mapRow][mapCol] = interactable
        self.removeFrontier(pRow, pCol)
        if (self.isGoal(pRow, pCol)):
            print("remove goal")
            print(self.goal)
            self.goal = None
            # todo - pop new goal
        #self.shouldInteract = False

    def flagBattle(self):
        # confirm to the world walker that it's okay he didn't move
        self.justBattled = True
        # retroactively mark any surrounding walls as unknown
        for direction in range(4):
            deltaRow, deltaCol = self.directionDelta(direction)
            pRow, pCol = self.playerRow + deltaRow, self.playerCol + deltaCol
            mapRow, mapCol = self.toMap((pRow, pCol))
            if (self.map[mapRow][mapCol]==wall):
                self.map[mapRow][mapCol] = unknown

    def movePlayer(self, pRow, pCol, direction):
        # player before and after coordinates in map space
        mapPlayerRow, mapPlayerCol = self.toMap((self.playerRow, self.playerCol))
        mapRow, mapCol = self.toMap((pRow, pCol))

        # remove player from old location
        if (self.map[mapPlayerRow][mapPlayerCol]!=start and self.map[mapPlayerRow][mapPlayerCol]!=door):
            self.map[mapPlayerRow][mapPlayerCol] = ground

        # add player to new location
        if (self.map[mapRow][mapCol]!=start and self.map[mapRow][mapCol]!=door):
            self.map[mapRow][mapCol] = player
        self.playerRow = pRow
        self.playerCol = pCol

        # check for map expansion
        self.expandMap(direction)

    def update(self, x, y):
        print("update with x,y = %d,%d" % (x,y))
        deltaRow, deltaCol = self.directionDelta(self.direction)
        expectedX, expectedY = self.x + deltaCol, self.y - deltaRow # convert between x,y and row,col
        pRow, pCol = self.playerRow + deltaRow, self.playerCol + deltaCol
        mapPlayerRow, mapPlayerCol = self.toMap((self.playerRow, self.playerCol))
        mapRow, mapCol = self.toMap((pRow, pCol))
        self.prevX = self.x
        self.prevY = self.y
        self.x = x
        self.y = y

        # check for warp
        if (not (self.x==expectedX and self.y==expectedY) and not (self.x==self.prevX and self.y==self.prevY)):
            print("moved more than expected!")
            print("before:")
            print((self.prevX, self.prevY))
            print("actual:")
            print((self.x,self.y))
            if (self.x!=self.prevX and self.y!=self.prevY):
                print("both x and y changed, assuming we warped")
                self.warp()
            else:
                changeX = self.x-self.prevX
                changeY = self.y-self.prevY
                # check for jumped over a hump. X or Y has changed by 2
                if (changeX==0 and abs(changeY)==2):
                    self.movePlayer(self.playerRow+changeY, self.playerCol)
                elif (changeY==0 and abs(changeX)==2):
                    self.movePlayer(self.playerRow, self.playerCol+changeX)
                else:
                    print("didn't consider this a warp or a hump")
        elif (self.shouldInteract):
            self.shouldInteract = False
        elif (self.changingDirection):
            self.changingDirection = False
            # sometimes if you time it just right
            # you can walk in the new direction on the first press
            if (self.x==expectedX and self.y==expectedY):
                # remove from frontier
                self.removeFrontier(pRow, pCol)
                if (self.map[mapPlayerRow][mapPlayerCol]!=start and self.map[mapPlayerRow][mapPlayerCol]!=door):
                    self.map[mapPlayerRow][mapPlayerCol] = ground
                if (self.map[mapRow][mapCol]!=start and self.map[mapRow][mapCol]!=door):
                    self.map[mapRow][mapCol] = player
                self.playerRow = pRow
                self.playerCol = pCol
                self.expandMap(self.direction) # add a row/column based on movement
        elif (self.justBattled):
            self.justBattled = False        
        elif (self.x==expectedX and self.y==expectedY):
            #print("prev xy: %d, %d" % (self.prevX, self.prevY))
            #print("delt xy: %d, %d" % (deltaCol, -deltaRow))
            #print("curr xy: %d, %d" % (self.x, self.y))
            #print("moved as expected")
            # remove from frontier
            self.removeFrontier(pRow, pCol)
            if (self.map[mapPlayerRow][mapPlayerCol]!=start and self.map[mapPlayerRow][mapPlayerCol]!=door):
                self.map[mapPlayerRow][mapPlayerCol] = ground
            if (self.map[mapRow][mapCol]!=start and self.map[mapRow][mapCol]!=door):
                self.map[mapRow][mapCol] = player
            self.playerRow = pRow
            self.playerCol = pCol
            self.expandMap(self.direction) # add a row/column based on movement
        elif (self.x==self.prevX and self.y==self.prevY):
            #print("ran into obstacle!")
            # there is a wall where you wanted to go
            if (self.map[mapRow][mapCol]!=start and self.map[mapRow][mapCol]!=door):
                self.map[mapRow][mapCol] = wall
            # remove this from the frontier
            self.removeFrontier(pRow, pCol)
            # flag to interact with this next time step
            self.shouldInteract = True
        else:
            print("moved more than expected!")
            print("before:")
            print((self.prevX, self.prevY))
            print("actual:")
            print((self.x,self.y))
            self.reset()
            
