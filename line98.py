import pygame, sys
import math, time


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
        self.row                = row
        self.col                = column
        self.x                  = row * GAP
        self.y                  = column * GAP
        self.width              = GAP
        self.color              = WHITE
        self.neighbours         = []
    
    # Get position of a square
    def getPosition(self):
        return self.row, self.col
    
    # Draw a square
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
    
    # Get the neighbour squares all round this square
    def getNeighbours(self, grid):
        self.neighbours = []

        # Below square
        if self.row < ROWS - 1:
            self.neighbours.append(grid[self.row + 1][self.col])
        
        # Upper square
        if self.row > 0:
            self.neighbours.append(grid[self.row - 1][self.col])
        
        # Right square
        if self.col < ROWS - 1:
            self.neighbours.append(grid[self.row][self.col + 1])
        
        # Left square
        if self.col > 0:
            self.neighbours.append(grid[self.row][self.col - 1])
        
        return self.neighbours
        
    # %%%%%%%%%%%%% Check status of the square %%%%%%%%%%%%% #
    def isIdle(self):
        return self.color == WHITE
        
    def isPath(self):
        return self.color == GREEN
    
    def isSelected(self):
        return self.color == TURQUOISE
    
    # %%%%%%%%%%%%% Change the status of the square %%%%%%%%%%%%% #
    def makePath(self):
        self.color = GREEN
    
    def makeIdle(self):
        self.color = WHITE
    
    def makeSelected(self):
        self.color = TURQUOISE



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



def reconstructPath(prev, grid, end, draw):
    path = []
    endRow, endCol = end.getPosition()
    current = (endRow, endCol)

    while current is not None:
        # grid[current[0]][current[1]].makePath()
        path.append(grid[current[0]][current[1]])
        current = prev[current[0]][current[1]]
        
    return path
    



# ========================== Breadth First Search Algorithm ========================== #
def findTheShortestWay(draw, grid, start, end):
    distance 		= [[-1 for spot in range(ROWS + 1)] for row in range(ROWS + 1)]
    prev 			= [[None for spot in range(ROWS + 1)] for row in range(ROWS + 1)]
    path = []

    from collections import deque
    rowQueue = deque()
    colQueue = deque()

    startRow, startCol = start.getPosition()
    endRow, endCol = end.getPosition()

    rowQueue.append(startRow)
    colQueue.append(startCol)
    distance[startRow][startCol] = 0

    while len(rowQueue) > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        row = rowQueue.popleft()
        col = colQueue.popleft()
        square = grid[row][col]

        if row == endRow and col == endCol:
            path = reconstructPath(prev, grid, end, draw)
            path.reverse()
            print('Find the way!!!')
            
            step = 0
            while step < len(path):
                movingSquare = path[step]
                movingSquare.makePath()
                draw()

                time.sleep(0.1)
                
                if step != len(path) - 1:
                    path[step].makeIdle()
                
                step += 1
            
            return path

        if row != endRow and col != endCol:
            print('Looking through neighbours!!!')
        
        for neighbour in square.getNeighbours(grid):
            neighRow, neighCol = neighbour.getPosition()

            if distance[neighRow][neighCol] == -1:
                distance[neighRow][neighCol] = distance[row][col] + 1
                rowQueue.append(neighRow)
                colQueue.append(neighCol)

                prev[neighRow][neighCol] = (row, col)
        
        draw()
    
    return None

        


    
def main():
    grid = makeGrid()
    selectedSquare = None
    end = None

    clock = pygame.time.Clock()

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
                    square.makeIdle()
                    selectedSquare = None
                
                elif not end and selectedSquare != square:
                    end = square
                    for row in grid:
                        for square in row:
                            square.getNeighbours(grid)
                        
                    findTheShortestWay(lambda: draw(WIN, ROWS, WIDTH, grid), grid, selectedSquare, end)
                    selectedSquare = None
                    end = None           

                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    selectedSquare = None
                    end = None
                    grid = makeGrid()

    pygame.quit()


main()