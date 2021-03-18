import pygame
import sys
import math
import time
import random


pygame.init()
# Window's Configuration
WIDTH = 450  # height and width of window
ROWS = 9  # rows and columns of the game's grid
GAP = WIDTH // ROWS  # width of each sqaure
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("LINE 98")

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

# List contains colors for alive square
SQUARE_COLORS = [ORANGE, BLUE, RED]

# Represent each square in the game's grid


class Square:
    def __init__(self, row, column):
        self.row = row
        self.col = column
        self.x = row * GAP
        self.y = column * GAP
        self.width = GAP
        self.color = WHITE
        self.movableRoutes = []
        self.isAlive = False
        self.originalColor = random.choice(SQUARE_COLORS)

        # Node Neighbours
        self.hNeigh = [self]
        self.vNeighs = [self]
        self.leftDNeighs = [self]
        self.rightDNeighs = [self]

    # Get position of a square
    def getPosition(self):
        return self.row, self.col

    # Draw a square
    def draw(self, win):
        reducedSize = 0 if not self.isAlive else 10
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width - reducedSize, self.width -reducedSize))

    # Get the movable squares all round this square
    def getMovableSquare(self, grid):
        self.movableRoutes = []

        # Below square
        if self.row < ROWS - 1 and grid[self.row + 1][self.col].isIdle():
            self.movableRoutes.append(grid[self.row + 1][self.col])

        # Upper square
        if self.row > 0 and grid[self.row - 1][self.col].isIdle():
            self.movableRoutes.append(grid[self.row - 1][self.col])

        # Right square
        if self.col < ROWS - 1 and grid[self.row][self.col + 1].isIdle():
            self.movableRoutes.append(grid[self.row][self.col + 1])

        # Left square
        if self.col > 0 and grid[self.row][self.col - 1].isIdle():
            self.movableRoutes.append(grid[self.row][self.col - 1])

        return self.movableRoutes


    # %%%%%%%%%%%%% Check status of the square %%%%%%%%%%%%% #
    def isSame(self, otherSquare):
        if not otherSquare.isAlive or not self.isAlive:
            return False
        return self.originalColor == otherSquare.originalColor

    def isIdle(self):
        return self.color == WHITE

    def isPath(self):
        return self.color == GREEN

    def isSelected(self):
        return self.color == TURQUOISE

    # %%%%%%%%%%%%% Change the status of the square %%%%%%%%%%%%% #
    def makeIdle(self):
        self.color = WHITE

    def makePath(self):
        self.color = GREEN

    def makeSelected(self):
        self.color = TURQUOISE

    def makeAlive(self):
        self.isAlive = True
        self.color = self.originalColor
    
    def __str__(self):
        return f'({self.row}, {self.col}, {self.originalColor})'


# Make A grid To Contain All The Node
def makeGrid():
    grid = []

    for row in range(ROWS):
        grid.append([])
        for col in range(ROWS):
            square = Square(row, col)
            grid[row].append(square)

    return grid

# Checking grid
def checkingGrid(grid, drawFunction):
    totalSquares = 0

    # Check for 5 in a column
    for row in range(ROWS):
        tempVList = [grid[row][0], ]
        for col in range(ROWS - 1):
            if grid[row][col].isSame(grid[row][col + 1]):
                tempVList.append(grid[row][col + 1])
            
            else:
    
                tempVList = [grid[row][col + 1], ]
        
            if len(tempVList) >= 5:
                print('There are 5 in a column')
                for square in tempVList:
                    square.makeIdle()
                    print(square.col, square.row)
                    time.sleep(0.1)
                    drawFunction()
        
    # Check for 5 in a column
    for col in range(ROWS):
        tempHList = [grid[0][col], ]
        for row in range(ROWS - 1):
            if grid[row][col].isSame(grid[row + 1][col]):
                tempHList.append(grid[row + 1][col])
            
            else:
    
                tempHList = [grid[row + 1][col], ]
        
            if len(tempHList) >= 5:
                print('There are 5 in a row')
                for square in tempHList:
                    square.makeIdle()
                    print(square.col, square.row)
                    time.sleep(0.1)
                    drawFunction()
    
    
    
    


# Generate a random Square
def randomSquare(grid):
    row = random.randint(0, 8)
    col = random.randint(0, 8)
    ranSquare = grid[row][col]

    while not ranSquare.isIdle():
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        ranSquare = grid[row][col]

    return ranSquare


def threeRandomSquare(grid):
    squares = []
    while len(squares) < 0:
        randomSquare = randomSquare(grid)
        squares.append(randomSquare)

    return squares



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
        path.append(grid[current[0]][current[1]])
        current = prev[current[0]][current[1]]

    return path


# ========================== Breadth First Search Algorithm ========================== #
def findTheShortestWay(draw, grid, start, end):
    distance = [[-1 for spot in range(ROWS + 1)] for row in range(ROWS + 1)]
    prev = [[None for spot in range(ROWS + 1)] for row in range(ROWS + 1)]
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

            originalColor = start.originalColor

            step = 0
            while step < len(path):
                movingSquare = path[step]
                movingSquare.color = originalColor

                if step == len(path) - 1:
                    movingSquare.originalColor = originalColor

                draw()

                time.sleep(0.07)

                if step != len(path) - 1:
                    path[step].makeIdle()

                step += 1

            return True

        if row != endRow and col != endCol:
            # print('Looking through movableRoutes!!!')
            pass

        for neighbour in square.getMovableSquare(grid):
            neighRow, neighCol = neighbour.getPosition()

            if distance[neighRow][neighCol] == -1:
                distance[neighRow][neighCol] = distance[row][col] + 1
                rowQueue.append(neighRow)
                colQueue.append(neighCol)

                prev[neighRow][neighCol] = (row, col)

        draw()

    return False


def main():
    grid = makeGrid()

    selectedSquare = None
    end = None

    firstSquare = randomSquare(grid)

    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(60)
        draw(WIN, ROWS, WIDTH, grid)
        checkingGrid(grid, lambda: draw(WIN, ROWS, WIDTH, grid))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = getClikedPos(pos)
                square = grid[row][col]

                if not selectedSquare and not square.isIdle():
                    square.makeSelected()
                    selectedSquare = square

                elif square.isSelected():
                    square.makeAlive()
                    selectedSquare = None

                elif selectedSquare and selectedSquare != square and square.isIdle():
                    end = square
                    for row in grid:
                        for square in row:
                            square.getMovableSquare(grid)

                    move = findTheShortestWay(
                        lambda: draw(WIN, ROWS, WIDTH, grid), grid, selectedSquare, end
                    )

                    if move:
                        selectedSquare = None
                        end = None
                        
                        i = 0
                        while i < 3:
                            randomSquare(grid)
                            i += 1

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    selectedSquare = None
                    end = None
                    grid = makeGrid()
                    
                    randomSquare(grid)

    pygame.quit()


main()
