import threading
import queue        
from tkinter import Tk, Canvas, Button
import random, time

class Gui():
    """
        This class takes care of the game's graphic user interface (gui)
        creation and termination.
    """
    def __init__(self):
        """        
            The initializer instantiates the main window and 
            creates the starting icons for the snake and the prey,
            and displays the initial gamer score.
        """
        #some GUI constants
        scoreTextXLocation = 60
        scoreTextYLocation = 15
        textColour = "white"
        #instantiate and create gui
        self.root = Tk()
        self.canvas = Canvas(self.root, width = WINDOW_WIDTH, 
            height = WINDOW_HEIGHT, bg = BACKGROUND_COLOUR)
        self.canvas.pack()
        #create starting game icons for snake and the prey
        self.snakeIcon = self.canvas.create_line(
            (0, 0), (0, 0), fill=ICON_COLOUR, width=SNAKE_ICON_WIDTH)
        self.preyIcon = self.canvas.create_rectangle(
            0, 0, 0, 0, fill=ICON_COLOUR, outline=ICON_COLOUR)
        #display starting score of 0
        self.score = self.canvas.create_text(
            scoreTextXLocation, scoreTextYLocation, fill=textColour, 
            text='Your Score: 0', font=("Helvetica","11","bold"))
        #binding the arrow keys to be able to control the snake
        for key in ("Left", "Right", "Up", "Down"):
            self.root.bind(f"<Key-{key}>", game.whenAnArrowKeyIsPressed)

        # ---- DEBUG -----
        # for x in range(0, WINDOW_WIDTH -1, 10):
        #     for y in range(0, WINDOW_HEIGHT -1, 10):
        #         self.canvas.create_oval(x, y, x+1, y+1, fill='red')

        # for x in range(5, WINDOW_WIDTH - 1, 10):
        #     for y in range(5, WINDOW_HEIGHT -1, 10):
        #         self.canvas.create_oval(x, y, x+1, y+1, fill='blue')

    def gameOver(self):
        """
            Displays game over at the end of the game
        """
        gameOverButton = Button(self.canvas, text="Game Over!", 
            height = 3, width = 10, font=("Helvetica","14","bold"), 
            command=self.root.destroy)
        self.canvas.create_window(200, 100, anchor="nw", window=gameOverButton)
    

class QueueHandler():
    """
        This class implements the queue handler for the game.
    """
    def __init__(self):
        self.queue = gameQueue
        self.gui = gui
        self.queueHandler()
    
    def queueHandler(self):
        '''
            Constantly retrieves tasks from the queue
        '''
        try:
            while True:
                task = self.queue.get_nowait()
                if "game_over" in task:
                    gui.gameOver()
                elif "move" in task:
                    points = [x for point in task["move"] for x in point]
                    gui.canvas.coords(gui.snakeIcon, *points)
                elif "prey" in task:
                    gui.canvas.coords(gui.preyIcon, *task["prey"])
                elif "score" in task:
                    gui.canvas.itemconfigure(
                        gui.score, text=f"Your Score: {task['score']}")
                self.queue.task_done()
        except queue.Empty:
            gui.root.after(100, self.queueHandler)


class Game():
    '''
        This class implements most of the game functionalities.
    '''
    def __init__(self):
        """
           This initializer sets the initial snake coordinate list, movement
           direction, and arranges for the first prey to be created.
        """
        self.queue = gameQueue
        self.score = 0
        #starting length and location of the snake
        #note that it is a list of tuples, each being an
        # (x, y) tuple. Initially its size is 5 tuples.       
        self.snakeCoordinates = [(495, 55), (485, 55), (475, 55),
                                 (465, 55), (455, 55)]
        #initial direction of the snake
        self.direction = "Left"
        self.gameNotOver = True
        self.createNewPrey()

    def superloop(self) -> None:
        """
            This method implements a main loop
            of the game. It constantly generates "move" 
            tasks to cause the constant movement of the snake.
            Use the SPEED constant to set how often the move tasks
            are generated.
        """
        SPEED = 0.15     #speed of snake updates (sec)
        while self.gameNotOver:
            #complete the method implementation below
            self.move()
            gameQueue.put({"move" : self.snakeCoordinates})            
            time.sleep(SPEED)
            # pass #remove this line from your implementation

    def whenAnArrowKeyIsPressed(self, e) -> None:
        """ 
            This method is bound to the arrow keys
            and is called when one of those is clicked.
            It sets the movement direction based on 
            the key that was pressed by the gamer.
            Use as is.
        """
        currentDirection = self.direction
        #ignore invalid keys
        if (currentDirection == "Left" and e.keysym == "Right" or 
            currentDirection == "Right" and e.keysym == "Left" or
            currentDirection == "Up" and e.keysym == "Down" or
            currentDirection == "Down" and e.keysym == "Up"):
            return
        self.direction = e.keysym

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
        #complete the method implementation below
        self.isGameOver(NewSnakeCoordinates) # check if game is over
        self.snakeCoordinates.append(NewSnakeCoordinates)

        # check if new coordinates overlap prey coords
        # if (NewSnakeCoordinates[0]-5 <= self.preyCoordinates[0] <= NewSnakeCoordinates[0]+5 )\
        #     and (NewSnakeCoordinates[1]-5 <= self.preyCoordinates[1] <= NewSnakeCoordinates[1]+5) :
        if (NewSnakeCoordinates == self.preyCoordinates):
            self.score += 1
            gameQueue.put({"score" : self.score}) # increment score
            self.createNewPrey() # if eaten, effectively extend the length by not deleting the oldest coord
        else :
            self.snakeCoordinates.pop(0) # if not eaten, length remains the same, delete oldest coord

        # check if 


        # Append the newest coord
        

    def calculateNewCoordinates(self) -> tuple:
        """
            This method calculates and returns the new 
            coordinates to be added to the snake
            coordinates list based on the movement
            direction and the current coordinate of 
            head of the snake.
            It is used by the move() method.    
        """
        lastX, lastY = self.snakeCoordinates[-1]
        
        #complete the method implementation below
        if self.direction == "Up":
            newCoordinates = (lastX,lastY-RESOLUTION)
        elif self.direction == "Down":
            newCoordinates = (lastX,lastY+RESOLUTION)
        elif self.direction == "Left":
            newCoordinates = (lastX-RESOLUTION, lastY)
        else:
            newCoordinates = (lastX+RESOLUTION, lastY)
        
        return newCoordinates

        
            
    def isGameOver(self, snakeCoordinates) -> None:
        """
            This method checks if the game is over by 
            checking if now the snake has passed any wall
            or if it has bit itself.
            If that is the case, it updates the gameNotOver 
            field and also adds a "game_over" task to the queue. 
        """
        x, y = snakeCoordinates

        outOfBounds = False
        if x <= 0 or y <= 0 or x >= WINDOW_WIDTH or y >= WINDOW_HEIGHT:
            outOfBounds = True

        bitItself = False

        for (x_existing, y_existing) in self.snakeCoordinates:
            if x == x_existing and y == y_existing:
                bitItself = True

        if outOfBounds or bitItself:
            self.gameNotOver = False
            gameQueue.put({"game_over"})
            

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
        THRESHOLD = 15   #sets how close prey can be to borders
        #complete the method implementation below
        
        # Note that when getting the range of the poossible spawn coords,
        # every coord must be a multiple of 5 not a 10 to ensure a sprite size of 10 
        # and to maintain the grid layout with gap of 10

        while True:
            x = random.randrange(THRESHOLD, WINDOW_WIDTH - THRESHOLD, 10)
            y = random.randrange(THRESHOLD, WINDOW_HEIGHT - THRESHOLD, 10)
            if (x,y) not in self.snakeCoordinates:
                break
        # offset = random.randrange(-2,2)
        offset = 0
        x1 = x + offset - PREY_ICON_WIDTH//2
        y1 = y + offset - PREY_ICON_WIDTH//2
        x2 = x + offset + PREY_ICON_WIDTH//2
        y2 = y + offset + PREY_ICON_WIDTH//2
        
        self.preyCoordinates = (x,y)
        gameQueue.put({"prey" : (x1, y1, x2, y2)}) # this is blocking btw

if __name__ == "__main__":
    #some constants for our GUI
    WINDOW_WIDTH = 500         
    WINDOW_HEIGHT = 300
    RESOLUTION = 10
    SNAKE_ICON_WIDTH = 15
    PREY_ICON_WIDTH = 10
    #add the specified constant PREY_ICON_WIDTH here     

    BACKGROUND_COLOUR = "green"   #you may change this colour if you wish
    ICON_COLOUR = "yellow"        #you may change this colour if you wish

    gameQueue = queue.Queue()     #instantiate a queue object using python's queue class

    game = Game()        #instantiate the game object

    gui = Gui()    #instantiate the game user interface
    
    QueueHandler()  #instantiate the queue handler    
    
    #start a thread with the main loop of the game
    threading.Thread(target = game.superloop, daemon=True).start()

    #start the GUI's own event loop
    gui.root.mainloop()