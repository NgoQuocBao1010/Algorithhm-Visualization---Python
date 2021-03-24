import pygame
import random, time

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

# Ball's Images
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
        self.color = random.choice(list(IMAGES.keys()))
        self.bigImgFile = IMAGES[self.color].get('big')
        self.smallImgFile = IMAGES[self.color].get('small')
        self.mainImg = None

        # animation
        self.selected = False
        self.up = False
        self.offsetY = 0

        # Status
        self.baby = False
        self.alive = False

    def __str__(self):
        return f'Spot at {self.row}, {self.col}'
    
    # Get position of a square
    def getPosition(self):
        return self.row, self.col
    
    # Get the movable squares all round this square
    def getMovableSquare(self, grid):
        self.movableRoutes = []

        # Below square
        if self.row < ROWS - 1 and not grid[self.row + 1][self.col].alive:
            self.movableRoutes.append(grid[self.row + 1][self.col])

        # Upper square
        if self.row > 0 and not grid[self.row - 1][self.col].alive:
            self.movableRoutes.append(grid[self.row - 1][self.col])

        # Right square
        if self.col < COLS - 1 and not grid[self.row][self.col + 1].alive:
            self.movableRoutes.append(grid[self.row][self.col + 1])

        # Left square
        if self.col > 0 and not grid[self.row][self.col - 1].alive:
            self.movableRoutes.append(grid[self.row][self.col - 1])

        return self.movableRoutes
    
    # Check if 2 spots is the same type
    def isSame(self, otherSpot):
        if not self.alive or not otherSpot.alive:
            return False
        
        return self.color == otherSpot.color
    
    # Update new color
    def update(self, otherSpot):
        self.color = otherSpot.color
        self.bigImgFile = IMAGES[self.color].get('big')
        self.smallImg = IMAGES[self.color].get('small')
        # self.mainImg = WIN.blit(self.bigImgFile, (self.x, self.y))

    # Make spot became bigger
    def makeAlive(self):
        self.alive = True
        self.baby = False
    
    # Make spot became dead
    def makeDead(self):
        self.alive = False
        self.baby = False
    
    # Draw a square
    def draw(self, win):
        pygame.draw.rect(win, self.bgColor, (self.x, self.y, self.width, self.width))

        if self.alive:
            # bouncing animation
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
            self.mainImg = win.blit(self.bigImgFile, (self.x, newY))
    
        elif self.baby:
            newX = self.x + 15
            newY = self.y + 15
            self.mainImg = win.blit(self.smallImgFile, (newX, newY))



# $$$$$$$$$$$$********* Grid contains all the ball $$$$$$$$$$$$********* #
class Grid():
    def __init__(self):
        # Grid coordinate's config
        self.width = self.height = 450
        self.marginBottom = 20
        self.rows = self.cols = 9
        self.x = (WIN_WIDTH - self.width) / 2
        self.y = WIN_HEIGHT - self.height -  self.marginBottom
        
        # ...
        self.babies = []
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
    
    # draw the lines
    def drawLine(self, win):
        gap = self.width // self.rows
        for row in range(self.rows):
            pygame.draw.line(win, BLACK, (self.x, self.y + row * gap), (self.x + self.width, self.y + row * gap))
            for col in range(self.rows):
                pygame.draw.line(win, BLACK, (self.x + col * gap, self.y), (self.x + col * gap, self.y + self.width))
            
            self.rectangle = pygame.draw.rect(win, BLACK, (self.x, self.y, self.width, self.width), 2)

    # Draw the grid
    def draw(self, win):
        for row in self.grid:
            for spot in row:
                spot.draw(win)

        self.drawLine(win)
        
    # return a col and col of a random idle sqot
    def randomSquare(self):
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        ranSquare = self.grid[row][col]

        while ranSquare.alive:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            ranSquare = self.grid[row][col]

        return row, col

    # make 3 random babies
    def makeBabies(self):
        self.babies = []
        while len(self.babies) < 10:
            newRol, newCol = self.randomSquare()
            self.grid[newRol][newCol].baby = True
            self.babies.append(self.grid[newRol][newCol])

    # Reset grid to start new round with 3 grown and 3 baby spots
    def resetNewRound(self):
        self.createNewGrid()
        newSquares = []

        while len(newSquares) < 3:
            newRol, newCol = self.randomSquare()
            self.grid[newRol][newCol].alive = True
            newSquares.append(self.grid[newRol][newCol])
        
        self.makeBabies()
    
    # Make all babies bigger
    def grownUp(self):
        for spot in self.babies:
            if spot.baby:
                spot.makeAlive()
        
        self.babies = []
    
    # checking grid conditions
    def checking(self, drawFunc):
        changed = False
        deleteSpots = []

        # Check for 5 same spot in a row
        for row in range(self.rows):
            tempVList = [self.grid[row][0], ]
            for col in range(self.cols - 1):  
                if self.grid[row][col].isSame(self.grid[row][col + 1]):
                    tempVList.append(self.grid[row][col + 1])
                else:
        
                    tempVList = [self.grid[row][col + 1], ]
            
                if len(tempVList) >= 5:
                    print('There are 5 in a row')
                    changed = True
                    for spot in tempVList:
                        if spot not in deleteSpots:
                            deleteSpots.append(spot)
        
        # Check for 5 same spot in a column
        for col in range(self.cols):
            tempHList = [self.grid[0][col], ]
            for row in range(self.rows - 1):
                if self.grid[row][col].isSame(self.grid[row + 1][col]):
                    tempHList.append(self.grid[row + 1][col])
                else:
                    tempHList = [self.grid[row + 1][col], ]
            
                if len(tempHList) >= 5:
                    print('There are 5 in a column')
                    changed = True
                    for spot in tempHList:
                        if spot not in deleteSpots:
                            deleteSpots.append(spot)

        # Right to Left diaognal
        for col in range(5):
            for row in range(5):
                if (
                    self.grid[row][col].isSame(self.grid[row + 1][col + 1]) and 
                    self.grid[row + 1][col + 1].isSame(self.grid[row + 2][col + 2]) and 
                    self.grid[row + 2][col + 2].isSame(self.grid[row + 3][col + 3]) and 
                    self.grid[row + 3][col + 3].isSame(self.grid[row + 4][col + 4])
                ):
                    deleteSpots.append(self.grid[row][col]);
                    deleteSpots.append(self.grid[row + 1][col + 1]);
                    deleteSpots.append(self.grid[row + 2][col + 2]);
                    deleteSpots.append(self.grid[row + 3][col + 3]);
                    deleteSpots.append(self.grid[row + 4][col + 4]);
        

        # Left to Right diaognal
        for col in range(4, self.cols):
            for row in range(5):
                if (
                    self.grid[row][col].isSame(self.grid[row + 1][col - 1]) and 
                    self.grid[row + 1][col - 1].isSame(self.grid[row + 2][col - 2]) and 
                    self.grid[row + 2][col - 2].isSame(self.grid[row + 3][col - 3]) and 
                    self.grid[row + 3][col - 3].isSame(self.grid[row + 4][col - 4])
                ):
                    deleteSpots.append(self.grid[row][col]);
                    deleteSpots.append(self.grid[row + 1][col - 1]);
                    deleteSpots.append(self.grid[row + 2][col - 2]);
                    deleteSpots.append(self.grid[row + 3][col - 3]);
                    deleteSpots.append(self.grid[row + 4][col - 4]);

        for spot in deleteSpots:
            spot.makeDead()
            time.sleep(0.08)
            drawFunc()
        
        return changed

    # ****************** BFS Algorithm ****************** #
    def findShortestPath(self, start, end, drawFunc):
        distance = [[-1 for spot in range(self.rows + 1)] for row in range(self.rows + 1)]
        prev = [[None for spot in range(self.rows + 1)] for row in range(self.rows + 1)]
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
            square = self.grid[row][col]

            if row == endRow and col == endCol:
                path = self.reconstructPath(prev, end)
                path.reverse()

                img = start.bigImgFile
                orginalColor = start.color

                c_x, c_y = start.x, start.y
                start.makeDead()

                for spot in path:
                    newX, newY = spot.x, spot.y
                    while c_x != newX or c_y != newY:
                        if newX > c_x:
                            c_x += 1
                        elif newX < c_x:
                            c_x -= 1

                        if newY > c_y:
                            c_y += 1
                        elif newY < c_y:
                            c_y -= 1
                        
                        WIN.fill(WHITE)
                        self.draw(WIN)
                        WIN.blit(img, (c_x, c_y))
                        pygame.display.update()

                    c_x, c_y = spot.x, spot.y
                    if spot == path[-1]:
                        path[-1].makeDead()
                        path[-1].update(start)
                        path[-1].makeAlive()

                return True

            if row != endRow and col != endCol:
                # print('Looking through movableRoutes!!!')
                pass

            for neighbour in square.movableRoutes:
                neighRow, neighCol = neighbour.getPosition()

                if distance[neighRow][neighCol] == -1:
                    distance[neighRow][neighCol] = distance[row][col] + 1
                    rowQueue.append(neighRow)
                    colQueue.append(neighCol)

                    prev[neighRow][neighCol] = (row, col)

            drawFunc()
        return False

    # Reconstruct the path found by algorithm
    def reconstructPath(self, prev, end):
        path = []
        endRow, endCol = end.getPosition()
        current = (endRow, endCol)

        while current is not None:
            path.append(self.grid[current[0]][current[1]])
            current = prev[current[0]][current[1]]

        return path


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
    grid.resetNewRound()

    selectedSquare = None
    gotoSquare = None

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(90)
        grid.checking(lambda: draw(WIN, grid))
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
                    print(spot.color)
                    if not selectedSquare:
                        if spot.alive:
                            if not spot.selected:
                                spot.selected = True
                                selectedSquare = spot
                    
                    elif selectedSquare == spot:
                        spot.selected = False
                        selectedSquare = None

                    elif selectedSquare and spot != selectedSquare and not spot.alive:
                        selectedSquare.selected = False
                        gotoSquare = spot

                        for row in grid.grid:
                            for square in row:
                                square.getMovableSquare(grid.grid)
                        
                        move = grid.findShortestPath(
                            selectedSquare, gotoSquare, lambda: draw(WIN, grid)
                        )

                        if move:
                            changed = grid.checking(lambda: draw(WIN, grid))
                            selectedSquare = None
                            gotoSquare = None

                            if not changed:
                                grid.grownUp()
                                grid.makeBabies()
                        
                        else:
                            selectedSquare.selected = True
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    selectedSquare = None
                    gotoSquare = None
                    grid.resetNewRound()


main()