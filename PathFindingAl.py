import pygame
import math
from queue import PriorityQueue

# Window's Configuration
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Path finding Algorithm")

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


# Node config
class Spot:
	def __init__(self, row, col, width, total_rows):
		self.row 			= row
		self.col 			= col
		self.x 				= row * width
		self.y 				= col * width
		self.color 			= WHITE
		self.width 			= width
		self.neighbours 	= []
		self.total_rows		= total_rows


	def getPosition(self):
		return self.row, self.col


	# ======================== Determine The Color For Each Node ========================
	def reset(self):
		self.color = WHITE

	def makeVisited(self):
		self.color = RED

	def makeOpened(self):
		self.color = GREEN

	def makeBarrier(self):
		self.color = BLACK

	def makeStart(self):
		self.color = ORANGE

	def makeEnd(self):
		self.color = TURQUOISE

	# ======================== Check The State Of Node ========================
	def isVisited(self):
		return self.color == RED

	def isOpened(self):
		return self.color == GREEN

	def isBarrier(self):
		return self.color == BLACK

	def isStart(self):
		return self.color == ORANGE

	def isEnd(self):
		return self.color == TURQUOISE

	# Draw Node
	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))


# Make A grid To Contain All The Node
def makeGrid(rows, width):
	grid = []
	gap = width // rows

	for row in range(rows):
		grid.append([])
		for col in range(rows):
			spot = Spot(row, col, gap, rows)
			grid[row].append(spot)

	return grid


def drawGrid(win, rows, width):
	gap = width // rows
	for row in range(rows):
		pygame.draw.line(win, GREY, (0, row * gap), (width, row * gap))
		for col in range(rows):
			pygame.draw.line(win, GREY, (col * gap, 0), (col * gap, width))



def draw(win, rows, width, grid):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	drawGrid(win, rows, width)
	pygame.display.update()


# Get the col and row of the cliked Spot
def getClikedPos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col


def main(win, width):
	ROWS = 50
	grid = makeGrid(ROWS, width)

	start = None
	end = None

	run = True

	while run:
		draw(win, ROWS, width, grid)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]:
				pos = pygame.mouse.get_pos()
				row, col = getClikedPos(pos, ROWS, width)
				spot = grid[row][col]

				if not start and spot != end:
					start = spot
					start.makeStart()

				elif not end and spot != start:
					end = spot 
					end.makeEnd()

				elif spot != end and spot != start:
					spot.makeBarrier()

	pygame.quit()




main(WIN, WIDTH)









