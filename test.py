import pygame

# Pygame initilize
pygame.init()
pygame.font.init()

# Window's Configuration
WIDTH = HEIGHT = 600                                        # height and width of window
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


# Draw the grid
def drawGrid(win, winWidth):
    rows = 9
    width = 450
    
    x = (winWidth - width) / 2
    y = winWidth - 20 - width

    gap = width / rows
    for row in range(rows):
        pygame.draw.line(win, BLACK, (x, y + row * gap), (x + width, y + row * gap))
        for col in range(rows):
            pygame.draw.line(win, BLACK, (x + col * gap, y), (x + col * gap, y + width))

    pygame.draw.rect(win, BLACK, (x, y, width, width), 2)


def draw(win, width):
    win.fill(WHITE)
    drawGrid(win , width)
    pygame.display.update()


# Get the col and row of the cliked Spot
def getClikedPos(pos):
    x, y = pos

    x = x - 75
    y = y - (600 - 450 - 20)

    row = y // 50
    col = x // 50

    return row, col


def main():
    run = True

    while run:
        draw(WIN, WIDTH)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = getClikedPos(pos)
                print(row, col)


main()
