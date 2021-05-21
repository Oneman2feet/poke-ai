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

# ASCII tiles for map
unknown = '/'
start = 'X'
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
        self.reset()
        
    def reset(self):
        self.changingDirection = False
        self.origin = [1, 1]
        self.map = [[unknown, unknown, unknown], [unknown, start, unknown], [unknown, unknown, unknown]]
        self.frontier = [ (1, 0), (0, 1) ]
        self.goal = None
        self.playerRow = 0
        self.playerCol = 0
        
    # most coordinates are with respect to the player starting position as 0,0
    # first coordinate is always the row and second the column
    # to convert this to the map coordinates, we translate by the location of the player start (origin)
    def toMap(self, rowCol):
        return (rowCol[0]+self.origin[0], rowCol[1]+self.origin[1])
    def fromMap(self, rowCol):
        return (rowCol[0]-self.origin[0], rowCol[1]-self.origin[1])

    def printMap(self):
        for row in self.map:
            print("\n", end =" "),
            for entry in row: 
                print(entry, end = " "),
        print("\n")
        
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
        elif (item==wall or item==interactable or item==start):
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

    def action(self):
        # choose where to go based on the map
        while (self.goal==None or (self.playerRow==self.goal[0] and self.playerCol==self.goal[1])):
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
            self.map[goalRow][goalCol] = impossible
            # check for traps
            if (len(self.frontier)==0):
                return empty
            # grab from the frontier
            self.goal = self.frontier.pop()
            path = self.pathfind()
        # show goal on map
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
        if (self.direction==0):
            return (0, 1)
        elif (self.direction==1):
            return (1, 0)
        elif (self.direction==2):
            return (0, -1)
        else:
            return (-1, 0)
    
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

    def flagInteraction(self):
        deltaRow, deltaCol = self.directionDelta(self.direction)
        pRow, pCol = self.playerRow + deltaRow, self.playerCol + deltaCol
        mapRow, mapCol = self.toMap((pRow, pCol))
        if (self.map[mapRow][mapCol]!=start):
            self.map[mapRow][mapCol] = interactable
        self.removeFrontier(pRow, pCol)

    def update(self, x, y):
        deltaRow, deltaCol = self.directionDelta(self.direction)
        expectedX, expectedY = self.x + deltaCol, self.y - deltaRow # convert between x,y and row,col
        pRow, pCol = self.playerRow + deltaRow, self.playerCol + deltaCol
        mapPlayerRow, mapPlayerCol = self.toMap((self.playerRow, self.playerCol))
        mapRow, mapCol = self.toMap((pRow, pCol))
        self.prevX = self.x
        self.prevY = self.y
        self.x = x
        self.y = y
        if (self.changingDirection):
            self.changingDirection = False        
        elif (self.x==expectedX and self.y==expectedY):
            #print("prev xy: %d, %d" % (self.prevX, self.prevY))
            #print("delt xy: %d, %d" % (deltaCol, -deltaRow))
            #print("curr xy: %d, %d" % (self.x, self.y))
            #print("moved as expected")
            # remove from frontier
            self.removeFrontier(pRow, pCol)
            if (self.map[mapPlayerRow][mapPlayerCol]!=start):
                self.map[mapPlayerRow][mapPlayerCol] = ground
            if (self.map[mapRow][mapCol]!=start):
                self.map[mapRow][mapCol] = player
            self.playerRow = pRow
            self.playerCol = pCol
            self.expandMap(self.direction) # add a row/column based on movement
        else:
            # there is a wall where you wanted to go
            if (self.map[mapRow][mapCol]!=start):
                self.map[mapRow][mapCol] = wall
            # remove this from the frontier
            self.removeFrontier(pRow, pCol)


