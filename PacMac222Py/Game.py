
from GameObject import GameObject

from GameDefs import globals
from GameDefs import SpriteType

from GameDefs import Pos
from Pill import Pill
from PacMan import PacMan
from Ghost import Ghost




class Game:

#You can simplify the game by changing these:
    addWalls = True
    numSmartGhosts = 1
    numGhosts = 2
    outsideWalls = False

    gameTime = 0



    def __init__(self):
        ghostPositions = [ Pos(1,1), Pos(26,26), Pos(2,2), Pos(25,25),  Pos(3,3), Pos(24,24), Pos(4,5), Pos(23,23) ]
            
        # Initialize game elements
        self.pacman = PacMan(Pos(15, 15))

        
        self.pill = Pill(Pos(15, 3))
        self.pill2 = Pill(Pos(15, 29))
        self.score = 0
        self.grid = [[None for x in range(globals.gameSize)] for y in range(globals.gameSize)]

        self.pills = [self.pill,self.pill2]
        self.ghosts = []
        for i in range(Game.numGhosts):
            if i < Game.numSmartGhosts:
                newGhost = Ghost(ghostPositions[i],0)
            else:
                newGhost = Ghost(ghostPositions[i],1)
            
               
            self.ghosts.append(newGhost)
            
        globals.pacman = self.pacman
        globals.ghosts = self.ghosts
        globals.pills = self.pills
        globals.pill_active = False


        if Game.outsideWalls:
            for i in range(globals.gameSize):
                GameObject(Pos(i, 0), SpriteType.WALL)
                GameObject(Pos(i, globals.gameSize - 1), SpriteType.WALL)
                GameObject(Pos(0, i), SpriteType.WALL)
                GameObject(Pos(globals.gameSize - 1, i), SpriteType.WALL)

        if Game.addWalls:


            for i in range(globals.gameSize  // 2 - 3):
                GameObject(Pos(i + globals.gameSize  // 4 + 2, globals.gameSize  // 4), SpriteType.WALL)
                GameObject(Pos(i + globals.gameSize  // 4 + 2, globals.gameSize  * 3 // 4), SpriteType.WALL)

                GameObject(Pos(globals.gameSize  // 4, i + globals.gameSize  // 4 + 2), SpriteType.WALL)
                GameObject(Pos(globals.gameSize  * 3 // 4, i + globals.gameSize  // 4 + 2), SpriteType.WALL)
        for i in range(globals.gameSize):
            for j in range(globals.gameSize):
                if GameObject.checkCollisions(Pos(i, j)) == SpriteType.EMPTY:
                    self.grid[i][j] = GameObject(Pos(i, j), SpriteType.DOT)

    def update(self):
        Game.gameTime += 1



        if self.grid[self.pacman.position.x][self.pacman.position.y] != None:
            self.grid[self.pacman.position.x][self.pacman.position.y].hide()
            self.grid[self.pacman.position.x][self.pacman.position.y] = None
            self.score += 1

        # Update game elements
        self.pacman.update()
        
        globals.pill_active = False
        for pill in self.pills:
            pill.update()

            if pill.isActive():
                globals.pill_active = True
            if self.pacman.checkCollision(pill):
                pill.eaten()
                
        for ghost in self.ghosts:
            ghost.update()
            if self.pacman.checkCollision(ghost):
                if globals.pill_active:
                    ghost.hide()
                    self.score += 100
                else:
                    print("Score: " + str(self.score))
                    return True

        if Game.gameTime >= 2000:
            print("Score: " + str(self.score))
            return True

        return False
    @staticmethod
    def check_xy(x,y):
        for obj in GameObject.gameObjects:
            if obj.position.x == x and obj.position.y == y:
                return obj.type
        return SpriteType.EMPTY
        
    @staticmethod
    def checkPosition(p):
        for obj in GameObject.gameObjects:
            if obj.position.x == p.x and obj.position.y == p.y:
                return obj.type
        return SpriteType.EMPTY

