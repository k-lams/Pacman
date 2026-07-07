import random
from GameObject import GameObject
from GameDefs import Pos, SpriteType, Direction, globals

class PacMan(GameObject):
    def __init__(self, p):
        super().__init__(p, SpriteType.PACMAN)
        self.ghostPositions = []
        self.dotPositions = []
        self.pillPositions = []
        self.lastMove = None
        self.previousGhostPositions = {}

    def updatePositions(self):
        self.ghostPositions = [Pos(x, y) for x in range(globals.gameSize) for y in range(globals.gameSize)
                               if globals.game.check_xy(x, y) == SpriteType.GHOST]
        self.dotPositions = [Pos(x, y) for x in range(globals.gameSize) for y in range(globals.gameSize)
                              if globals.game.check_xy(x, y) == SpriteType.DOT]
        self.pillPositions = [Pos(x, y) for x in range(globals.gameSize) for y in range(globals.gameSize)
                              if globals.game.check_xy(x, y) == SpriteType.PILL]

        for i, ghost in enumerate(globals.ghosts):
            self.previousGhostPositions[i] = ghost.position

    def getSafeDirections(self):
        possibleMoves = {
            Direction.UP: (self.position.x, self.position.y - 1),
            Direction.DOWN: (self.position.x, self.position.y + 1),
            Direction.LEFT: (self.position.x - 1, self.position.y),
            Direction.RIGHT: (self.position.x + 1, self.position.y),
            Direction.UPLEFT: (self.position.x - 1, self.position.y - 1),
            Direction.UPRIGHT: (self.position.x + 1, self.position.y - 1),
            Direction.DOWNLEFT: (self.position.x - 1, self.position.y + 1),
            Direction.DOWNRIGHT: (self.position.x + 1, self.position.y + 1),
        }

        safeMoves = [d for d, (x, y) in possibleMoves.items()
                     if globals.game.check_xy(x, y) not in [SpriteType.GHOST, SpriteType.WALL]]

        if not safeMoves:
            return list(possibleMoves.keys())

        predictedGhostPositions = [self.predictGhostMovement(ghost) for ghost in globals.ghosts]
        nearestGhost = self.findNearest(SpriteType.GHOST)

        if nearestGhost and self.getDistance(self.position, nearestGhost) <= 3:
            for predicted in predictedGhostPositions:
                if self.getDistance(self.position, predicted) <= 2:
                    if self.lastMove in safeMoves:
                        safeMoves.remove(self.lastMove)

        return safeMoves if safeMoves else list(possibleMoves.keys())

    def move(self):
        self.updatePositions()
        nearestGhost = self.findNearest(SpriteType.GHOST)

        # Move towards ghosts if pill is active
        if globals.pill_active and nearestGhost:
            move = self.moveTowards(nearestGhost)
            self.lastMove = move
            return move

        if nearestGhost and self.getDistance(self.position, nearestGhost) <= 3:
            move = self.moveAwayFromGhosts()
            self.lastMove = move
            return move

        nearestPill = self.findNearest(SpriteType.PILL)
        if nearestPill and self.getDistance(self.position, nearestPill) <= 6:
            move = self.moveTowards(nearestPill)
            self.lastMove = move
            return move

        dotPos = self.findNearest(SpriteType.DOT)
        if dotPos:
            move = self.moveTowards(dotPos)
            self.lastMove = move
            return move

        move = self.explore()
        self.lastMove = move
        return move

    def findNearest(self, targetType):
        bestDist = float('inf')
        bestPos = None

        positions = self.ghostPositions if targetType == SpriteType.GHOST else self.dotPositions

        for targetPos in positions:
            dist = self.getDistance(self.position, targetPos)
            if dist < bestDist:
                bestDist = dist
                bestPos = targetPos

        return bestPos

    def moveTowards(self, targetPos):
        dx, dy = targetPos.x - self.position.x, targetPos.y - self.position.y

        if abs(dx) >= abs(dy):
            prioritisedMoves = [
                (Direction.RIGHT, dx > 0), (Direction.LEFT, dx < 0),
                (Direction.UP, dy < 0), (Direction.DOWN, dy > 0),
                (Direction.UPRIGHT, dx > 0 and dy < 0), (Direction.UPLEFT, dx < 0 and dy < 0),
                (Direction.DOWNRIGHT, dx > 0 and dy > 0), (Direction.DOWNLEFT, dx < 0 and dy > 0)
            ]
        else:
            prioritisedMoves = [
                (Direction.UP, dy < 0), (Direction.DOWN, dy > 0),
                (Direction.RIGHT, dx > 0), (Direction.LEFT, dx < 0),
                (Direction.UPRIGHT, dx > 0 and dy < 0), (Direction.UPLEFT, dx < 0 and dy < 0),
                (Direction.DOWNRIGHT, dx > 0 and dy > 0), (Direction.DOWNLEFT, dx < 0 and dy > 0)
            ]

        for move, valid in prioritisedMoves:
            if valid and move in self.getSafeDirections():
                return move

        return random.choice(self.getSafeDirections())

    def moveAwayFromGhosts(self):
        safeMoves = self.getSafeDirections()

        bestMove = None
        maxSafety = -float('inf')

        predictedGhostPositions = [self.predictGhostMovement(ghost) for ghost in globals.ghosts]

        for move in safeMoves:
            newX, newY = self.position.x, self.position.y

            if move == Direction.UP:
                newY -= 1
            elif move == Direction.DOWN:
                newY += 1
            elif move == Direction.LEFT:
                newX -= 1
            elif move == Direction.RIGHT:
                newX += 1
            elif move == Direction.UPLEFT:
                newX -= 1
                newY -= 1
            elif move == Direction.UPRIGHT:
                newX += 1
                newY -= 1
            elif move == Direction.DOWNLEFT:
                newX -= 1
                newY += 1
            elif move == Direction.DOWNRIGHT:
                newX += 1
                newY += 1

            newPos = Pos(newX, newY)

            minDistToGhost = min(self.getDistance(newPos, ghost.position) for ghost in globals.ghosts)
            minPredDistToGhost = min(self.getDistance(newPos, predicted) for predicted in predictedGhostPositions)

            safetyScore = minDistToGhost + minPredDistToGhost

            if safetyScore > maxSafety:
                bestMove = move
                maxSafety = safetyScore

        if bestMove is None:
            bestMove = random.choice(safeMoves)

        return bestMove

    def predictGhostMovement(self, ghost):
        currentPos = ghost.position

        dx = 0
        dy = 0

        if currentPos.x < self.position.x:
            dx = 1
        elif currentPos.x > self.position.x:
            dx = -1

        if currentPos.y < self.position.y:
            dy = 1
        elif currentPos.y > self.position.y:
            dy = -1

        predictedPos = Pos(currentPos.x + dx, currentPos.y + dy)

        return predictedPos

    def explore(self):
        # Look for areas with dots and pills and avoid ghost clusters
        if self.dotPositions:
            nearestDot = self.findNearest(SpriteType.DOT)
            return self.moveTowards(nearestDot)

        return random.choice(self.getSafeDirections())

    def getDistance(self, pos1, pos2):
        return abs(pos1.x - pos2.x) + abs(pos1.y - pos2.y)
