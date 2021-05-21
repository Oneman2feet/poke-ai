#!/usr/bin/python

import time
import random

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

class World:     

    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.prevX = x
        self.prevY = y
        self.direction = direction
        self.changingDirection = False
        # char in map entry keeps track of type of square
        # '?' is an unknown square, 'P' is the player's current position, 'W' is a warp 
        # 'B' is a 'block' - impassible square, "D" means sign or sprite (opens dialogue box when clicked)
        # 'S' is a 'safe' square - player can move on it freely
        self.origin = [0, 0]
        self.map = [["?","?","?"],["?","P","?"],["?","?","?"]]
        self.frontier = [(0, 1), (1, 0), (1, 2), (2, 1)]
        self.goal = [1, 2]
        self.path = None
        self.playerRow = 1
        self.playerCol = 1

    def printMap(self):
        for row in self.map:
            print("\n", end =" "),
            for entry in row: 
                print(entry, end = " "),
        print("\n")

    def cost(self, item):
        if (item=='?'):
            return 2
        elif (item=='S' or item=='P'):
            return 1
        elif (item=='B'):
            return 0
        else:
            return -1
        
    # return array of directions needed to move to the goal
    def pathfind(self):
        # convert map to cost matrix
        matrix = [ [ self.cost(item) for item in row ] for row in self.map ]
        # input to pathfinding algorithm
        grid = Grid(matrix=matrix)
        # determine start and end
        start = grid.node(self.playerRow+self.origin[0], self.playerCol+self.origin[1])
        end = grid.node(self.goal[0]+self.origin[0], self.goal[1]+self.origin[1])
        finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
        path, runs = finder.find_path(start, end, grid)
        return path

    def directionTo(self, position):
        rowDiff = position[0] - (self.playerRow + self.origin[0])
        colDiff = position[1] - (self.playerCol + self.origin[1])
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
            # grab from the frontier
            print("new goal")
            self.goal = self.frontier.pop()
        # pathfind to goal
        self.path = self.pathfind()
        # get next step
        newPosition = self.path.pop(1)
        # determine direction to next step
        newDirection = self.directionTo(newPosition)
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
    
    def expandMap(self, direction):
        if (self.direction==0 and self.playerCol==len(self.map[0])-1-self.origin[1]):
            # add element at end of each row
            for row in self.map:
                row.append('?')
            # player position does not change
        elif (self.direction==1 and self.playerRow==len(self.map)-1-self.origin[0]):
            # add new row at end
            self.map.append(['?']*len(self.map[0]))
            # player position does not change
        elif (self.direction==2 and self.playerCol==self.origin[1]):
            # add element at start of each row
            for row in self.map:
                row.insert(0, '?')
            # shift map origin column by one
            self.origin[1] += 1
        elif (self.playerRow==self.origin[0]):
            # add new row at beginning
            self.map.insert(0, ['?']*len(self.map[0]))
            # shift map origin row by one
            self.origin[0] += 1
            

    def update(self, x, y):
        deltaRow, deltaCol = self.directionDelta(self.direction)
        expectedX, expectedY = self.x + deltaCol, self.y - deltaRow # convert between x,y and row,col
        pRow, pCol = self.playerRow + deltaRow, self.playerCol + deltaCol
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
            self.map[self.playerRow+self.origin[0]][self.playerCol+self.origin[1]] = 'S'
            self.map[pRow+self.origin[0]][pCol+self.origin[1]] = 'P'
            self.playerRow = pRow
            self.playerCol = pCol
            self.expandMap(self.direction) # add a row/column based on movement
        else:
            #print("hit something")
            # there is a wall where you wanted to go
            self.map[pRow+self.origin[0]][pCol+self.origin[1]] = 'B'
            # pick a new direction
            self.direction = (self.direction + 1) % 4
            self.changingDirection = True





    def getPath(self): 
        #when called, perhaps empty stack? (for recalculating path if wall found)
        self.pathStack.clear()
        self.searchStack.clear()
        self.prevStack.clear()
        #A* search - basically depth first search in this case 
        #Starting node is the player's current location (represented by playerX and playerY)
        #start by pushing the starting node to the stack, then begin loop. 
        rowIndex = -1
        entryIndex = -1
        for row in self.currentMap:
            rowIndex = rowIndex + 1
            entryIndex = -1 
            for entry in row:
                entryIndex = entryIndex + 1
                if (entry == "P"): 
                    #print("Found player at index (" + str(rowIndex) + " , " + str(entryIndex) + ") \n"),
                    #first entry in the tuple is the type of square, next two entries are the row and column indices, fourth entry is the path length, final entry is the directional instructions to reach that space
                    self.searchStack.append(("P", rowIndex, entryIndex, 0.0, "NONE"))
                    #print("Adding starting space to the search stack. Search stack = " + str(self.searchStack) + "\n")
        #loop - search stack for shortest path, pop that node 
        currentEntry = None
        #print("Entering While loop \n")
        while (len(self.searchStack) > 0):
            lowestPathLength = float("Inf")  
            currentEntry = None
            #print("About to begin searching the stack \n") 
            for entry in self.searchStack:
                    #print("searchStack entry is " + str(entry) + "\n")
                    if (entry[3] < lowestPathLength): 
                        #print("New shortest path found - old path was " + str(lowestPathLength) + ", new path is " + str(entry[3]) + "\n")
                        currentEntry = entry
                        lowestPathLength = currentEntry[3]
            #print("Current shortest path is through the entry " + str(currentEntry) + "\n")
        #check if node is a destination - if so, break out of loop and start backtracking
            self.searchStack.remove(currentEntry)
            #print("Removing current entry from search stack. Search stack is now " + str(self.searchStack) + "\n")
            self.prevStack.append(currentEntry)
            #print("Adding current entry to previous stack. Previous stack is now " + str(self.prevStack) + "\n")             
            if(currentEntry[0] == "?"):
                #print("Found an unknown space at " + str(currentEntry) + "\n") 
                break
        #if not, expand node by creating left, up, right, and down children (identified by array position) else: 
                #expand to the left (x - 1) 
            #print("About to expand the current entry") 
            currentRow = currentEntry[1]
            currentColumn = currentEntry[2]
            currentCost = currentEntry[3]
            if (currentColumn != 0):
                leftEntry = self.currentMap[currentRow][currentColumn - 1]
                stepCost = self.getStepCost(leftEntry)
                #print("Current cost = " + str(currentCost) + ", step cost = " + str(stepCost) + ", left entry = " + leftEntry + "\n")
                self.searchStack.append((leftEntry, currentRow, currentColumn - 1, currentCost + stepCost, "LEFT"))
                #print("Adding left entry. Search stack is now " + str(self.searchStack) + "\n")
            if (currentRow != 0): 
                upEntry = self.currentMap[currentRow -1][currentColumn]
                stepCost = self.getStepCost(upEntry)
                self.searchStack.append((upEntry, currentRow - 1, currentColumn, currentCost + stepCost, "UP"))
               # print("Adding up entry. Search stack is now " + str(self.searchStack) + "\n")
            if(currentColumn < len(self.currentMap[currentRow]) - 1): 
                rightEntry = self.currentMap[currentRow][currentColumn + 1]
                stepCost = self.getStepCost(rightEntry)
                self.searchStack.append((rightEntry, currentRow, currentColumn + 1, currentCost + stepCost, "RIGHT"))
                #print("Adding right entry. Search stack is now " + str(self.searchStack) + "\n")
            if(currentRow < len(self.currentMap) - 1): 
                downEntry = self.currentMap[currentRow + 1][currentColumn]
                stepCost = self.getStepCost(downEntry)
                self.searchStack.append((downEntry, currentRow + 1, currentColumn, currentCost + stepCost, "DOWN"))
               # print("Adding down entry. Search stack is now " + str(self.searchStack) + "\n") 
    #backtracking - once a destination node is found, add its direction to the pathStack and loop until you make your way back to the start node
        if (currentEntry[0] == "?"): 
            #print("Beginning backtracking with " + str(currentEntry) + "\n")
            while (currentEntry[0] != "P"): 
                direction = currentEntry[4]
                self.pathStack.append(direction)
                #print("Adding direction to pathstack - pathStack is now " + str(self.pathStack) + "\n")
                targetRow = None
                targetColumn = None
                #print("Locating previous step \n")
                if(direction == "LEFT"): 
                    targetRow = currentEntry[1]
                    targetColumn = currentEntry[2] + 1
                if(direction == "UP"): 
                    targetRow = currentEntry[1] + 1
                    targetColumn = currentEntry[2]
                if(direction == "RIGHT"):
                    targetRow = currentEntry[1]
                    targetColumn = currentEntry[2] - 1
                if(direction == "DOWN"): 
                    targetRow = currentEntry[1] - 1
                    targetColumn = currentEntry[2]
                for prev in self.prevStack: 
                    #print("Checking prev = " + str(prev) + "\n")
                    if(prev[1] == targetRow and prev[2] == targetColumn):
                        #print("Previous step found - " + str(prev) + "\n") 
                        currentEntry = prev
                        break
                self.prevStack.remove(currentEntry) 

    def getStepCost(self, currentEntry): 
        if (currentEntry == "B" or currentEntry == "D" or currentEntry == "P"): 
            stepCost = float("Inf")
        elif (currentEntry == "S" or currentEntry == "?"): 
            stepCost = 1.0
        elif (currentEntry == "W"): 
            stepCost = 1000.0
        return stepCost



    def returnAction(self): 
        if (self.xPos % 16 == 0 and self.yPos % 16 == 0):
            #TODO check if player actually moved or warped, adjust map accordingly, then take next action (this could be a separate called function
            #If player moved, update map to show current position (previous position goes from "player" to "safe"
            #also add new row / column of unknowns to the map in the direction of movement
            #if player did not move, update space they should have moved to as impassible (wall) 
            #if player hits wall, press A to see if dialogue box appears. To check for dialogue box, try moving in all directions. If cannot move any direction, dialogue box is open. If dialogue discovered, hammer A while occasionally checking for movement 
            #also check for warp / wraparound. Check wraparound values 
            #to check for warp - check if both x and y changed (should not be possible in other circumstances)
            #If either x and y were already 0 then warp could be confused for movement - check if the non-zero value changed by more than one. In rare occasions this may be confused for a wraparound, but its the best I can do right now
            if (len(self.pathStack) == 0):  
                self.getPath()
            nextStep = self.pathStack.pop()
            print("Popping next step - next step = " + nextStep + "\n")
            if nextStep == "LEFT":
                self.direction = "LEFT"
                return [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]                
            elif nextStep == "RIGHT":
                self.direction = "RIGHT"
                return [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]                     
            elif nextStep == "UP":
                self.direction = "UP"
                return [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]                    
            elif nextStep == "DOWN":
                self.direction = "DOWN"
                return [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0] 
            elif nextStep == "CHECK":
                self.direction = "CHECK"
                return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]                   
            elif nextStep == "RANDOM": 
                randNum = int(random.random() * 4)
                if (randNum == 0):
                    self.direction = "UP"
                    return [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]                        
                elif (randNum == 1): 
                    self.direction = "DOWN"
                    return [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]                        
                elif (randNum == 2): 
                    self.direction = "LEFT"
                    return [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]                        
                else:
                    self.direction = "RIGHT"
                    return [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]  
            else: 
                self.direction == "NONE"
                return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]                        

