
from GameObject import GameObject
from GameDefs import SpriteType
from GameDefs import Direction
from GameDefs import globals
from GameDefs import Pos
class Ghost(GameObject):
    def __init__(self, p, ghost_type):
        super().__init__(p, SpriteType.GHOST)
        self.ghostType = ghost_type
        
 

    def avoid_walls(self, dx, dy):
        pacman_pos = globals.pacman.position
        dist = abs(pacman_pos.x - self.position.x) + abs(pacman_pos.y - self.position.y)
        
        

        newPos = Pos((self.position.x ) % globals.gameSize, (self.position.y  ) % globals.gameSize)
        
        #look ahead for wall
        for i in range(max(dist,10)):
            newPos = Pos((newPos.x + dx) % globals.gameSize, (newPos.y + dy) % globals.gameSize)
                
            if globals.game.checkPosition(newPos) == SpriteType.WALL:
   
                possible_directions = [(0,-1),(0,1),(-1,0),(1,0)]
                wall_directions = []
                for direction in possible_directions:
                    testPos = Pos((newPos.x + direction[0]) % globals.gameSize, (newPos.y + direction[1]) %globals.gameSize)
                    if globals.game.checkPosition(testPos) == SpriteType.WALL:
                         wall_directions.append(direction)
                #aim for next to corner
                if len(wall_directions) == 1:
                    dx = - wall_directions[0][0]
                    dy = - wall_directions[0][1]
                    return dx,dy
                    
                
                best = 90
                bestPos = []

#look for the nearest gap in the wall               
                for w in wall_directions:
                    for i in range(30):
                        testPos = Pos((newPos.x + w[0]*i) % globals.gameSize, (newPos.y + w[1]*i) %globals.gameSize)
                        if globals.game.checkPosition(testPos) != SpriteType.WALL:
                            break
                    if i < best:
                        best = i
                        bestPos = testPos
                
                dx, dy = self.get_dxdy_to(bestPos.x,bestPos.y)

                if globals.game.check_xy(self.position.x+dx,self.position.y+dy) == SpriteType.WALL:
                    #don't get stuck on wall
                    if globals.game.check_xy(self.position.x+dx,self.position.y+0) != SpriteType.WALL:
                        dy = 0
                    else:
                        dx = 0
                return dx,dy

        # If no wall was encountered, return the original direction
        return dx, dy

    def get_dxdy_to(self, x,y):
        game_size = globals.gameSize
        my_pos = self.position
        dx = (x - my_pos.x + game_size) % game_size
        dy = (y - my_pos.y + game_size) % game_size

        # Adjust for wrap-around
        if dx > game_size // 2:
            dx -= game_size
        if dy > game_size // 2:
            dy -= game_size

	    # Limit the movement to one step
        dx = max(-1, min(1, dx))
        dy = max(-1, min(1, dy))
        return dx,dy
        
    def move_good(self):
        direction = Direction.NONE
        
        if self.loopCount %3 ==0:
            return direction
                        
        game_size = globals.gameSize
        pacman_pos = globals.pacman.position
        my_pos = self.position

        
        dx, dy = self.get_dxdy_to(pacman_pos.x,pacman_pos.y)
        
        dx, dy = self.avoid_walls(dx, dy)

        # Reverse direction if pill is active (run away instead of chase)
        if globals.pill_active:
            dx = -dx
            dy = -dy

        # Determine direction
  
        
        if dy > 0:
            direction |= Direction.DOWN
        if dy < 0:
            direction |= Direction.UP
        if dx > 0:
            direction |= Direction.RIGHT
        if dx < 0:
            direction |= Direction.LEFT

      
        return direction
        
    def move_quick(self):
        direction = Direction.NONE
        
        
                
        if globals.pacman.position.y > self.position.y:
            direction =  Direction.DOWN
        if globals.pacman.position.y < self.position.y:
            direction = Direction.UP
        if globals.pacman.position.x > self.position.x:
            direction = Direction.RIGHT
        if globals.pacman.position.x < self.position.x:
            direction = Direction.LEFT

        
        return direction    
        
    def move(self):
        
        if self.ghostType == 1:
            return self.move_quick()
        return self.move_good()
            
        
        
