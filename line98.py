import pygame
from pygame.locals import *


# Pygame initilize
pygame.init()
pygame.font.init()


# Window's Configuration
WIDTH = HEIGHT = 450                                        # height and width of window
ROWS = COLS = 9                                             # rows and columns of the game's grid
GAP = WIDTH // ROWS                                         # width of each sqaure
WIN = pygame.display.set_mode((WIDTH, WIDTH))               # initilize win form
pygame.display.set_caption("LINE 98")                       # win caption

# Color Variables
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


img = pygame.image.load("images/big1.png")

class Spot():
    def __init__(self, row, column):
        self.row = row
        self.col = column
        self.x = self.col * GAP
        self.y = self.row * GAP
        self.width = GAP
        self.color = WHITE

        # animation
        self.up = False
        self.offsetY = 0
    
    # Get position of a square
    def getPosition(self):
        return self.row, self.col
    
    # Draw a square
    def draw(self, win):
        if self.color != WHITE:
            if not self.up:
                self.offsetY += 1
            
            if self.offsetY == 10:
                self.up = True
            
            if self.up:
                self.offsetY -= 1
            
            if self.offsetY < 0:
                self.offsetY = 0
                self.up = False
            
            newY = self.y - self.offsetY
            win.blit(img, (self.x, newY))
            # img.render(win, (self.x, self.y))
        else:
            pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))


# Grid of the game
class Grid():
    def __init__(self):
        self.grid = []

        for row in range(ROWS):
            self.grid.append([])

            for col in range(COLS):
                spot = Spot(row, col)
                self.grid[row].append(spot)
    

    def draw(self, win, rows, width):
        for row in self.grid:
            for spot in row:
                spot.draw(win)


        gap = width // rows
        for row in range(rows):
            pygame.draw.line(win, GREY, (0, row * gap), (width, row * gap))
            for col in range(rows):
                pygame.draw.line(win, GREY, (col * gap, 0), (col * gap, width))




# Draw the whole window
def draw(win, rows, width, grid):
    win.fill(WHITE)
    grid.draw(win, rows, width)
    pygame.display.update()


# Get the col and row of the cliked Spot
def getClikedPos(pos):
    x, y = pos

    row = y // GAP
    col = x // GAP

    return row, col

def main():
    grid = Grid()

    rectangles = []
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)
        draw(WIN, ROWS, WIDTH, grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = getClikedPos(pos)
                spot = grid.grid[row][col]
                spot.color =  RED
                # rectangles.append((row, col))


main()