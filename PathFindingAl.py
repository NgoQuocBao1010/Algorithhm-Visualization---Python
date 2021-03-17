import pygame
import math
from queue import PriorityQueue

# Window's Configuration
WIDTH = 900
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

	def makePath(self):
		self.color = PURPLE

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

	# Get the neighbours of the spot:
	def getNeighbours(self, grid):
		self.neighbours = []

		# Check the below spot
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].isBarrier():
			self.neighbours.append(grid[self.row + 1][self.col])

		# Check the above spot
		if self.row > 0 and not grid[self.row - 1][self.col].isBarrier():
			self.neighbours.append(grid[self.row - 1][self.col])

		# Check the right spot
		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].isBarrier():
			self.neighbours.append(grid[self.row][self.col + 1])

		# Check the below spot
		if self.col > 0 and not grid[self.row][self.col - 1].isBarrier():
			self.neighbours.append(grid[self.row][self.col - 1])

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


def reconstructPath(prev, grid, end, draw):
	e_row, e_col = end.getPosition()
	current = (e_row, e_col)
	while current is not None:
		grid[current[0]][current[1]].makePath()
		current = prev[current[0]][current[1]]


# ========================== Breadth First Search Algorithm ========================== #
def algorithm(draw, grid, start, end):
	rows = len(grid)
	print(rows)
	distance 		= [[-1 for spot in range(rows + 1)] for row in range(rows + 1)]
	prev 			= [[None for spot in range(rows + 1)] for row in range(rows + 1)]

	from collections import deque
	row_queue = deque()
	col_queue = deque()

	s_row, s_col = start.getPosition()
	e_row, e_col = end.getPosition()

	row_queue.append(s_row)
	col_queue.append(s_col)
	distance[s_row][s_col] = 0

	while len(row_queue) > 0:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		row = row_queue.popleft()
		col = col_queue.popleft()
		spot = grid[row][col]

		if row == e_row and col == e_col:
			reconstructPath(prev, grid, end, draw)
			end.makeEnd()
			start.makeStart()
			return True

		if row != s_row and col != s_col:
			spot.makeVisited()

		for neighbour in spot.neighbours:
			n_row, n_col = neighbour.getPosition()

			if distance[n_row][n_col] == -1:
				distance[n_row][n_col] = distance[row][col] + 1
				row_queue.append(n_row)
				col_queue.append(n_col)
				prev[n_row][n_col] = (row, col)
				grid[n_row][n_col].makeOpened()
			else:
				spot.makeVisited()
		draw()


	return False





def main(win, width):
	ROWS = 9
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

			elif pygame.mouse.get_pressed()[2]:
				pos = pygame.mouse.get_pos()
				row, col = getClikedPos(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()

				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for spot in row:
							spot.getNeighbours(grid)
					algorithm(lambda: draw(win, ROWS, width, grid), grid, start, end)

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = makeGrid(ROWS, width)


	pygame.quit()




main(WIN, WIDTH)









