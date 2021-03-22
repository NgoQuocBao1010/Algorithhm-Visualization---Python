import pygame
import random

# Pygame initilize
pygame.init()
pygame.font.init()

# Window's Configuration
WIN_WIDTH = WIN_HEIGHT = 600                                # height and width of window
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_WIDTH))       # initilize win form
pygame.display.set_caption("LINE 98")                       # win caption


# Grid Configuration
WIDTH = HEIGHT = 450                                        # width and height of the grid
GAP = 50                                                    # width of each square in a grid
ROWS = COLS = 9

# Color Variables
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Images Container
IMAGES = {
    'yellow': {
        'big': pygame.image.load('./images/big1.png'),
        'small': pygame.image.load('./images/small1.png'),
    },
    'pink': {
        'big': pygame.image.load('./images/big2.png'),
        'small': pygame.image.load('./images/small2.png'),
    },
    'blue': {
        'big': pygame.image.load('./images/big3.png'),
        'small': pygame.image.load('./images/small3.png'),
    },
    'green': {
        'big': pygame.image.load('./images/big4.png'),
        'small': pygame.image.load('./images/small4.png'),
    },
    'red': {
        'big': pygame.image.load('./images/big5.png'),
        'small': pygame.image.load('./images/small5.png'),
    },
}


# Each square in the grid
class Spot():
    def __init__(self, row, column):
        self.row = row
        self.col = column
        self.x = self.col * GAP + 75
        self.y = self.row * GAP + 130
        self.width = GAP

        # Spot status
        self.bgColor = WHITE
        self.color = 'green'

        # animation
        self.selected = False
        self.up = False
        self.offsetY = 0

        # Status
        self.alive = False
    
    # Get position of a square
    def getPosition(self):
        return self.row, self.col
    
    # Draw a square
    def draw(self, win):
        pygame.draw.rect(win, self.bgColor, (self.x, self.y, self.width, self.width))

        if self.alive:
            if self.selected:
                if not self.up:
                    self.offsetY += 1
            
                if self.offsetY == 10:
                    self.up = True
                
                if self.up:
                    self.offsetY -= 1
                
                if self.offsetY < 0:
                    self.offsetY = 0
                    self.up = False
            
            else:
                self.offsetY = 0
            
            newY = self.y - self.offsetY
            win.blit(IMAGES[self.color].get('big'), (self.x, newY))


# Grid contains all the ball
class Grid():
    def __init__(self):
        # Grid coordinate's config
        self.width = self.height = 450
        self.marginBottom = 20
        self.rows = self.cols = 9
        self.x = (WIN_WIDTH - self.width) / 2
        self.y = WIN_HEIGHT - self.height -  self.marginBottom
        
        self.createNewGrid()
    
    # check if the mouse is clicked inside grid
    def isCliked(self, pos):
        mouseX, mouseY = pos

        if mouseX < self.x or mouseX > self.x + self.width:
            return False
        
        if mouseY < self.y or mouseY > self.y + self.height:
            return False

        return True
    
    # Return the row and col of the spot that was clicked
    def getPosition(self, pos):
        mouseX, mouseY = pos

        spotX = mouseX - self.x
        spotY = mouseY - (WIN_HEIGHT - self.height - self.marginBottom)

        spotRow = spotY // GAP
        spotCol = spotX // GAP
        
        return int(spotRow), int(spotCol)

    # Initialize a empty grid
    def createNewGrid(self):
        self.grid = []

        for row in range(ROWS):
            self.grid.append([])

            for col in range(COLS):
                spot = Spot(row, col)
                self.grid[row].append(spot)

    # Draw the grid
    def draw(self, win):
        for row in self.grid:
            for spot in row:
                spot.draw(win)


        gap = self.width // self.rows
        for row in range(self.rows):
            pygame.draw.line(win, BLACK, (self.x, self.y + row * gap), (self.x + self.width, self.y + row * gap))
            for col in range(self.rows):
                pygame.draw.line(win, BLACK, (self.x + col * gap, self.y), (self.x + col * gap, self.y + self.width))
        

        self.rectangle = pygame.draw.rect(win, BLACK, (self.x, self.y, self.width, self.width), 2)


    # generate a random square in grid
    def randomSquare(self):
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        ranSquare = self.grid[row][col]

        while ranSquare.alive:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            ranSquare = self.grid[row][col]

        self.grid[row][col].alive = True




def draw(win, grid):
    win.fill(WHITE)
    grid.draw(win)
    pygame.display.update()


# Get the col and row of the cliked Spot
def getClikedPos(pos):
    x, y = pos
    
    return x, y


def main():
    grid = Grid()
    grid.randomSquare()

    selectedSquare = None

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)
        draw(WIN, grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                
                if grid.isCliked(pos):
                    row, col = grid.getPosition(pos)

                    spot = grid.grid[row][col]

                    if spot.alive and not selectedSquare:
                        spot.selected = True
                        selectedSquare = spot
                    
                    elif selectedSquare == spot:
                        print('Yes')
                        spot.selected = False
                        selectedSquare = None


main()