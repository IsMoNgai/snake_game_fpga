import pygame
import random
import time
import threading
from gameEntities import Snake, Prey

class Gui:
    """
        This class handles all GUI-related processing. 
        It's rendering is controlled by the GameEngine class,
        which contains the main game rendering loop.
    """
    def __init__(self):
        """        
            The initializer instantiates the main window and 
            creates the starting icons for the snake and the prey,
            and displays the initial player score.
        """
        # These are some GUI Constants
        self.scoreTextXLocation = 60
        self.scoreTextYLocation = 15
        textColour = (255, 255, 255)

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 20, bold=True)
        self.textColour = textColour
        self.backgroundColor = BACKGROUND_COLOUR 
        # The snakeCoordinates are delivered from the instantiated Game class.
        self.snakeCoordinates = game.playerSnake.coordinates 
        self.preyCoordinates = None
        self.score = 0
        self.screen.fill(self.backgroundColor)

        pygame.display.update() # Update the screen to show the latest staged object results

    """
        The following render* functions are called by the GameEngine class
        inside of the queueHandler method. The queueHandler method also acts as
        the main event loop for rendering the GUI elements.
    """
    def renderSnake(self) -> None:
        """
            Once called by the queueHandler/GUI render loop, this function renders the Snake.
        """
        if self.snakeCoordinates:
            # Draw each segment of the snake as a rectangle
            for coord in self.snakeCoordinates:
                # Stage this object to pygame
                rect = pygame.Rect(coord[0], coord[1], SNAKE_ICON_WIDTH, SNAKE_ICON_WIDTH)
                innerRect = pygame.Rect(coord[0] + SPRITE_BORDER, 
                                        coord[1] + SPRITE_BORDER, 
                                        SNAKE_ICON_WIDTH - 2*SPRITE_BORDER,
                                        SNAKE_ICON_WIDTH - 2*SPRITE_BORDER)
                pygame.draw.rect(self.screen, SNAKE_BORDER_COLOUR, rect)
                pygame.draw.rect(self.screen, SNAKE_FILL, innerRect)

    def renderPrey(self) -> None:
        """
            Once called by the queueHandler/GUI render loop, this function renders the Prey.
        """
        # Render prey and get snake coordinates from the event queue
        if self.preyCoordinates:
            x, y = self.preyCoordinates
            prey_rect = pygame.Rect(x, y, PREY_ICON_WIDTH, PREY_ICON_WIDTH)
            pygame.draw.rect(self.screen, PREY_COLOUR, prey_rect)

    def renderScore(self) -> None:
        """
            Renders the current score on the screen when called.
        """
        # Using blit to overlap this score suurface to the designated background location
        score_surface = self.font.render(f"Your Score: {self.score}", True, self.textColour)
        self.screen.blit(score_surface, (self.scoreTextXLocation, self.scoreTextYLocation))

    def gameOver(self) -> None:
        """
            Clears the screen and renders the Game Over message 
        """
        game_over_surface = self.font.render("Game Over!", True, self.textColour)
        # Centers this message on screen
        self.screen.blit(game_over_surface, ((WINDOW_WIDTH - game_over_surface.get_width()) // 2,
                                                (WINDOW_HEIGHT - game_over_surface.get_height()) // 2))
        pygame.display.update()


class GameEngine:
    """
        This handles the event receiving and the game loop.
        The Gui() class is instantiated as an object here, which 
        GameEngine controls.
        The events are collected and then sent directly to the gui object.
        Then, gui methods are called to then create the pygame objects/scenes that 
        represent the Snake, Prey, and game over screen.

        When the game is over, it will wait a little bit before auto-exiting.
    """
    def __init__(self):
        self.gui = gui  
        
    def queueHandler(self) -> None:

        running = True
        while running:
            self.gui.screen.fill(self.gui.backgroundColor) # First fill the background 

            # ===== GRID LAYOUT =====
            for i in range (0, WINDOW_WIDTH, RESOLUTION):
                    pygame.draw.line(self.gui.screen, "blue", [i, 0],[i, WINDOW_HEIGHT],1)
            for j in range (0, WINDOW_HEIGHT, RESOLUTION):
                    pygame.draw.line(self.gui.screen, "blue", [0, j],[WINDOW_WIDTH, j],1)
            
            game.whenAnArrowKeyIsPressed() # Detect player inputs

            for event in pygame.event.get(): # Process events 
                if event.type == pygame.QUIT:
                    running = False
                    self.gui.gameOver()

                elif event.type == MOVE:
                    self.gui.snakeCoordinates = event.move

                elif event.type == PREY:
                    self.gui.preyCoordinates = event.prey

                elif event.type == SCORE:
                    self.gui.score = event.score

            self.gui.renderPrey() # Create the game objects 
            self.gui.renderSnake()
            self.gui.renderScore()

            pygame.display.update()
            self.gui.clock.tick(40) # This dictate the frame rate. 
            # This is the time gap between frame renders in this while loop

        self.gui.gameOver() # Displays the game over screen
        time.sleep(2) # Wait a little bit before auto exiting
        pygame.quit()


class Game:
    '''
        This class implements most of the game functionalities.
        Much of the code is kept from part 1, except isGameOver 
        and detecting Keyboard inputs from the player.
        Updates regarding the status of the game is sent 
        to the GameEngine class via the pygame event queue.
    '''
    def __init__(self):
        """
           This initializer sets the initial snake coordinate list, movement
           direction, and arranges for the first prey to be created.
        """
        self.score = 0

        # self.snakeCoordinates = [(20*RESOLUTION, 3*RESOLUTION), 
        #                          (19*RESOLUTION, 3*RESOLUTION), 
        #                          (18*RESOLUTION, 3*RESOLUTION), 
        #                          (17*RESOLUTION, 3*RESOLUTION), 
        #                          (16*RESOLUTION, 3*RESOLUTION)]
        
        self.playerSnake = Snake(
            playable=False,
            spawnDirection="Left",
            spawnCoordinates=[(20*RESOLUTION, 3*RESOLUTION), 
                                 (19*RESOLUTION, 3*RESOLUTION), 
                                 (18*RESOLUTION, 3*RESOLUTION), 
                                 (17*RESOLUTION, 3*RESOLUTION), 
                                 (16*RESOLUTION, 3*RESOLUTION)],
            fillColour=SNAKE_FILL,
            borderColour=SNAKE_BORDER_COLOUR,
            allowedZone=(0,0,WINDOW_WIDTH,WINDOW_HEIGHT),
        )
        # self.direction = "Left"
        self.gameNotOver = True
        self.preyCoordinates = None
        self.createNewPrey()

    def superloop(self) -> None:
        """
            This method implements a main loop
            of the game. It constantly generates "move" 
            tasks to cause the constant movement of the snake.
            Use the SPEED constant to set how often the move tasks
            are generated.
        """
        SPEED = 0.1     # Speed of snake position updates (seconds)
        while self.gameNotOver:
            # self.move()

            if self.playerSnake.move(self.preyCoordinates, [(None)]) == True:
                self.score += 1
                pygame.event.post(pygame.event.Event(SCORE, {'score' : self.score}))
                self.createNewPrey()

            if self.playerSnake.alive == False:
                self.endGame()
            
            move_event = pygame.event.Event(MOVE, {"move" : self.playerSnake.coordinates})
            pygame.event.post(move_event)
            gui.clock.tick(60)
            time.sleep(SPEED)






    def whenAnArrowKeyIsPressed(self) -> None:
            """ 
                This method is called when one of the arrow keys is pressed.
                It sets the movement direction based on 
                the key that was pressed by the gamer.
                Use as is.
            """
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and self.playerSnake.direction != "Down":
                self.playerSnake.direction = "Up"
            elif keys[pygame.K_DOWN] and self.playerSnake.direction != "Up":
                self.playerSnake.direction = "Down"
            elif keys[pygame.K_LEFT] and self.playerSnake.direction != "Right":
                self.playerSnake.direction = "Left"
            elif keys[pygame.K_RIGHT] and self.playerSnake.direction != "Left":
                self.playerSnake.direction = "Right"






    def move(self) -> None:
        """ 
            This method implements what is needed to be done
            for the movement of the snake.
            It generates a new snake coordinate. 
            If based on this new movement, the prey has been 
            captured, it adds a task to the queue for the updated
            score and also creates a new prey.
            It also calls a corresponding method to check if 
            the game should be over. 
            The snake coordinates list (representing its length 
            and position) should be correctly updated.
        """
        NewSnakeCoordinates = self.calculateNewCoordinates()
        self.isGameOver(NewSnakeCoordinates)  # Check if game over
        self.snakeCoordinates.append(NewSnakeCoordinates)
        # Check if new coordinates overlap prey coords
        sx = NewSnakeCoordinates[0] # Snake X, Y
        sy = NewSnakeCoordinates[1]        
        px = self.preyCoordinates[0] 
        py = self.preyCoordinates[1]
      
        eaten = self.hasCapturedPrey(sx, sy, px, py)

        if eaten:
            self.score += 1
            pygame.event.post(pygame.event.Event(SCORE, {'score' : self.score}))
            self.createNewPrey()  # If eaten, effectively extend the length by not deleting the oldest coord
        else:
            self.snakeCoordinates.pop(0)  # If not eaten, length remains the same, delete oldest coord
    
    def hasCapturedPrey(self, sx, sy, px, py) -> bool:
        """
            Returns whether if a snake has eaten
            the prey given the snake and prey coordinates.
        """
        captured_flag : bool = (sx == px) and (sy == py)
        return captured_flag

    def calculateNewCoordinates(self) -> tuple: # AS IS
        """
            This method calculates and returns the new 
            coordinates to be added to the snake
            coordinates list based on the movement
            direction and the current coordinate of 
            head of the snake.
            It is used by the move() method.    
        """
        lastX, lastY = self.snakeCoordinates[-1]
  
        direction = self.direction
        
        if direction == "Up":
            newCoordinates = (lastX, lastY - RESOLUTION)
        elif direction == "Down":
            newCoordinates = (lastX, lastY + RESOLUTION)
        elif direction == "Left":
            newCoordinates = (lastX - RESOLUTION, lastY)
        else:
            newCoordinates = (lastX + RESOLUTION, lastY)

        return newCoordinates

    def isGameOver(self, snakeCoordinates) -> None:
        """
            This method checks if the game is over by 
            checking if now the snake has passed any wall
            or if it has bit itself.
            If that is the case, it updates the gameNotOver 
            field and also adds a "gameOverFlag" task to the queue. 
        """
        x, y = snakeCoordinates

        # Game ends when either of these conditions are met
        outOfBounds : bool = x < 0 or y < 0 or x >= WINDOW_WIDTH or y >= WINDOW_HEIGHT
        bitItself : bool = snakeCoordinates in self.snakeCoordinates

        if outOfBounds or bitItself:
            self.gameNotOver = False
            pygame.event.post(pygame.event.Event(pygame.QUIT))
    
    def endGame(self) -> None:
        self.gameNotOver = False
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    def createNewPrey(self) -> None:
        """ 
            This methods picks an x and a y randomly as the coordinate 
            of the new prey and uses that to calculate the 
            coordinates (x - 5, y - 5, x + 5, y + 5). [you need to replace 5 with a constant]
            It then adds a "prey" task to the queue with the calculated
            rectangle coordinates as its value. This is used by the 
            queue handler to represent the new prey.                    
            To make playing the game easier, set the x and y to be THRESHOLD
            away from the walls. 
        """
        THRESHOLD = 1*RESOLUTION   # This sets how close the prey can spawn to the border
        while True: # Keep trying to generate coordinates until valid.
            x = random.randrange(THRESHOLD, WINDOW_WIDTH - THRESHOLD, RESOLUTION)
            y = random.randrange(THRESHOLD, WINDOW_HEIGHT - THRESHOLD, RESOLUTION)
            if (x, y) not in self.playerSnake.coordinates:
                break

        self.preyCoordinates = (x, y)
        pygame.event.post(pygame.event.Event(PREY, {"prey" : self.preyCoordinates}))


if __name__ == "__main__":
    # GUI constants
    WINDOW_WIDTH = 500         
    WINDOW_HEIGHT = 500
    RESOLUTION = 20
    SNAKE_ICON_WIDTH = 20
    PREY_ICON_WIDTH = 20 
    SPRITE_BORDER = 3

    BACKGROUND_COLOUR = (64, 132, 128)  # Green 
    SNAKE_FILL = (128, 0, 148)      # Yellow 
    SNAKE_BORDER_COLOUR = (128, 0, 255)
    PREY_COLOUR = (255, 255, 0) 

    pygame.init()
    MOVE = pygame.USEREVENT + 1 # Custom pygame events are declared like this.
    PREY = pygame.USEREVENT + 2
    SCORE = pygame.USEREVENT + 3

    game = Game()  
    gui = Gui()
    engine = GameEngine() # initialize the game engine which contains the loop for
    # the GUI rendering. This also contains the queue system that is a part of pygame.
    
    threading.Thread(target = game.superloop, daemon=True).start() 
    # Starts the game logic loop as a daemon thread. 

    engine.queueHandler() # start the main loop of the game engine/ GUI renderer
