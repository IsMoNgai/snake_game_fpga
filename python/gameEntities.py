class Entity:
    """
        Parent class for all in-game entities
    """
    def __init__(self, *, 
                playable : bool, fillColour : tuple[3],
                borderColour : tuple[3], segmentSize : int = 20,
                allowedZone : tuple[4] = (0,0,400,400)
                ):
        self.playable = playable
        self.fillColour = fillColour
        self.borderColour = borderColour
        self.segmentSize = segmentSize
        self.allowedZone = allowedZone


class Prey(Entity):
    def __init__(self, *, 
                spawnCoordinates : tuple, 
                fillColour : tuple[3],
                borderColour : tuple[3],
                segmentSize : int = 20,
                allowedZone : tuple[4]
                ):
        
        super().__init__(
            playable=False, 
            fillColour=fillColour, 
            borderColour=borderColour, 
            segmentSize=segmentSize, allowedZone=allowedZone)
        
        self.coordinates = spawnCoordinates


class Snake(Entity):
    def __init__(self, *, 
                playable : bool,
                spawnDirection : str = "Left",
                spawnCoordinates : list[tuple], 
                score : int = 0,
                fillColour : tuple[3],
                borderColour : tuple[3],
                segmentSize : int = 20,
                allowedZone : tuple[4]
                ):
        
        super().__init__(playable=playable, 
                        fillColour=fillColour, 
                        borderColour=borderColour, 
                        segmentSize=segmentSize, allowedZone=allowedZone)
        
        self.direction = spawnDirection
        self.coordinates = spawnCoordinates
        self.score = score
        self.alive : bool = True

    def move(self, preyCoordinates : tuple[2], obstacleCoordinatesList : list[tuple]) -> bool:
        """
            Moving logic for the Snake
            Returns True if prey was eaten
        """
        newCoords = self.calculateNewCoordinates()

        # Check if new coordinates kills this snake
        # i.e., collided with an obstable (enemy snake), or hit wall

        inbounds : bool = (self.allowedZone[0] <= newCoords[0] <= self.allowedZone[2]) \
                            and (self.allowedZone[1] <= newCoords[1] <= self.allowedZone[3])
        hitEnemy : bool = False
        if obstacleCoordinatesList:
            for enemyCoord in obstacleCoordinatesList:
                if enemyCoord == newCoords:
                    hitEnemy = True
                    break
        if not inbounds or hitEnemy:
            self.alive = False # indicate that we are now dead
        
        # If we're still alive, check if we've now eaten a prey
        self.coordinates.append(newCoords)

        if newCoords == preyCoordinates:
            self.score += 1
            return True  # If eaten, effectively extend the length by not deleting the oldest coord
        else:
            self.coordinates.pop(0)  # If not eaten, length remains the same, delete oldest coord
            return False

    def calculateNewCoordinates(self) -> tuple:
        """
            This method calculates and returns the new 
            coordinates to be added to the snake
            coordinates list based on the movement
            direction and the current coordinate of 
            head of the snake.
            It is used by the move() method.    
        """
        lastX, lastY = self.coordinates[-1]
  
        direction = self.direction
        
        if direction == "Up":
            newCoordinates = (lastX, lastY - self.segmentSize)
        elif direction == "Down":
            newCoordinates = (lastX, lastY + self.segmentSize)
        elif direction == "Left":
            newCoordinates = (lastX - self.segmentSize, lastY)
        else:
            newCoordinates = (lastX + self.segmentSize, lastY)

        return newCoordinates

    
    