import pygame
from game_objects import *
from pygame.locals import *
from random import randint

class Map:
    def __init__(self, width = 20, height = 20):
        self.wall = Tile(pygame.image.load("res/map/wall.png").convert(), True)
        self.floor = Tile(pygame.image.load("res/map/floor.png").convert())
        self.pathTile = Tile(pygame.image.load("res/map/path.png").convert())
        self.map = []
        self.width = width
        self.height = height
        self.start = (1,1)
        self.end = (width-2,height-2)
        for y in range(0, height):
            row = []
            if (y == 0 or y == height - 1):
                for x in range(0, width):
                    row.append(self.wall)
            else:
                row.append(self.wall)
                for x in range(0, width - 2):
                    row.append(self.wall)
                row.append(self.wall)
            self.map.append(row)

        self.makePath()
        for i in range(0, len(self.path)):
            pos = self.path[i]
            xLoc = pos[0]
            yLoc = pos[1]
            self.map[yLoc][xLoc] = self.pathTile
    
    def isSolid(self, x, y):
        return self.map[y][x].solid
  
    def makePath(self):
        cLoc = self.start
        path = [] # array of positions
        path.append(cLoc)
           
        xBeg = self.start[0]
        yBeg = self.start[1]
        xEnd = self.end[0]
        yEnd = self.end[1]

        # the 'correct' direction to move
        xDir = yDir = 1
        if xEnd < xBeg: xDir = -1
        if yEnd < yBeg: yDir = -1

        check = 0
        
        while not(cLoc[0] is self.end[0] and cLoc[1] is self.end[1]):

            if check > 100: break
            check += 1        

            x = cLoc[0]
            y = cLoc[1]
            xDiff = abs(x-xEnd)
            yDiff = abs(y-yEnd)            
            
            goY = True
            if xDiff > 5 and yDiff > 5: # Doesnt matter which dir we go
                if randint(0,1) is 0: goY = False  # 50% of the time switch it up.
            else: # it DOES matter which dir we go because one of the directions is nearly "satisfied"
                if xDiff > yDiff: goY = False 

            otherMoves = []
            cMove = (x,y)
            if goY: # Determine if the best move on the X or Y axis
                cMove = (x,y+yDir)
                otherMoves.append((x+xDir,y))
                otherMoves.append((x-xDir,y))
            else:
                cMove = (x+xDir,y)
                otherMoves.append((x,y+yDir))
                otherMoves.append((x,y-yDir))

            
                
            # print "current x:%d, y:%d, correct move is to x:%d, y%d" % (x,y,cMove[0],cMove[1])

            validMoves = [] # Validate the possible moves
            for i in range(0,2):
                move = otherMoves[i]
                if move[0] > 0 and move[0] < self.width-1 and move[1] > 0 and move[1] < self.height-1: # Not going off map
                    if move not in path: # Not stepping over itself
                        validMoves.append(move)
                 
            choice = randint(0,len(validMoves)) # move towards goal or in rand Dir
            if choice is 0: #make the Correct move
                cLoc = cMove
            else: #make one of the random moves
                cLoc = validMoves[choice-1]
           
            # print "Number of valid moves is %d, choice number is %d" % (len(validMoves),choice)
 
            path.append(cLoc)
       
        #End While
 
        self.path = path
    #End makepath()
      
    def render(self, surface, xOffset, yOffset):
        width, height = surface.get_size()
        for y in range(0, len(self.map)):
            for x in range(0, len(self.map[y])):
                surface.blit(self.map[y][x].sprite, ((width / 2) - 25 - xOffset + (x * 50), (height / 2) - 25 - yOffset + (y * 50)))
