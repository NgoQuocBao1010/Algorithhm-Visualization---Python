import pygame, sys
import math


pygame.init()
# Window's Configuration
WIDTH = 450         # height and width of window
ROWS = 9            # rows and columns of the game's grid
GAP = WIDTH // ROWS # width of each sqaure
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("LINE 98")

# Color Variables
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Square:
    def __init__(self, row, column):
        self.x                  = row * GAP
        self.y                  = column * GAP
        self.width              = GAP
        self.color              = WHITE
        self.neighbour          = []
    
    # Get position of a square
    def getPosition(self):
        return self.x, self.y

    def isIdle(self):
        return self.color == WHITE
    
    def isSelected(self):
        return self.color == TURQUOISE
    
    def makeIdle(self):
        self.color = WHITE
    
    def makeSelected(self):
        self.color = TURQUOISE
    
    # Draw a square
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))


# Make A grid To Contain All The Node
def makeGrid():
	grid = []

	for row in range(ROWS):
		grid.append([])
		for col in range(ROWS):
			square = Square(row, col)
			grid[row].append(square)

	return grid



# Draw the grid
def drawGrid(win, rows, width):
	gap = width // rows
	for row in range(rows):
		pygame.draw.line(win, GREY, (0, row * gap), (width, row * gap))
		for col in range(rows):
			pygame.draw.line(win, GREY, (col * gap, 0), (col * gap, width))

# Draw the whole window
def draw(win, rows, width, grid):
    win.fill(WHITE)

    for row in grid:
        for square in row:
            square.draw(win)

    drawGrid(win, rows, width)
    pygame.display.update()


# Get the col and row of the cliked Spot
def getClikedPos(pos):
	y, x = pos

	row = y // GAP
	col = x // GAP

	return row, col


# ========================== Breadth First Search Algorithm ========================== #
def findTheShortestWay(draw, grid, start, end):
    distance 		= [[-1 for spot in range(ROWS + 1)] for row in range(ROWS + 1)]
    prev 			= [[None for spot in range(ROWS + 1)] for row in range(ROWS + 1)]

    from collections import deque
    rowQueue = deque()
    colQueue = deque()

    



    
def main():
    grid = makeGrid()
    selectedSquare = None

    run = True
    while run:
        draw(WIN, ROWS, WIDTH, grid)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = getClikedPos(pos)
                square = grid[row][col]

                if not selectedSquare:
                    square.makeSelected()
                    selectedSquare = square
                
                elif square.isSelected():
                    if square.isSelected():
                        square.makeIdle()
                        selectedSquare = None

        
    pygame.quit()


main()