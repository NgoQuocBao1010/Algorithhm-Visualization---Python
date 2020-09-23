import pygame
import random
import math
import time

pygame.init()
# Window's Configuration
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("DFS Algorithm")

# Images
nodesImages = [pygame.image.load('./images/1.png'),
			   pygame.image.load('./images/2.png'),
			   pygame.image.load('./images/3.png'),
			   pygame.image.load('./images/4.png'), 
			   pygame.image.load('./images/5.png'),
			   pygame.image.load('./images/6.png'),
			   pygame.image.load('./images/7.png'), 
			   pygame.image.load('./images/8.png'),
			   pygame.image.load('./images/9.png'),
			   pygame.image.load('./images/10.png'), ]

# Color Variables
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
BROWN = (146, 43, 33)
LIGHTGREEN = (26, 188, 156)
LIGHTPURPLE = (187, 143, 206)


# Node Config
class Node:
	def __init__(self, x, y, order):
		self.x = x
		self.y = y
		self.order = order
		self.radius = 47
		self.borderWidth = 5
		self.color = BLACK
		self.edges = []
		self.neighbours = []
		self.dragging = False
		self.clickedPosition = ()

	# Check if the mouse is above the Node
	def isAbove(self, point):
		p_x, p_y = point
		self.clickedPosition = (p_x, p_y)
		distance = math.sqrt((self.x - p_x) * (self.x - p_x) + (self.y - p_y) * (self.y - p_y))

		return distance <= self.radius

	def getCenterPosition(self):
		return self.x, self.y

	def draw(self, win):
		win.blit(nodesImages[self.order - 1], (self.x - 45, self.y - 43))
		pygame.draw.circle(win, self.color, (self.x, self.y), self.radius, self.borderWidth)

	# color config
	def reset(self):
		self.color = BLACK

	def makeDragged(self):
		self.color = GREEN

	def makeVisited(self):
		self.color = RED

	def makeOpened(self):
		self.color = GREEN

	# Special Method
	def __eq__(self, other):
		return other.x == self.x and other.y == self.y

	def __ne__(self, other):
		return other.x != self.x and other.y != self.y

	def __str__(self):
		return str(self.order)


# A grid to contain all the nodes
def makeGrid(nodes, width):
	grid = []
	nodes_set = []

	while len(nodes_set) < nodes:
		x = random.randint(50, width - 45)
		y = random.randint(50, width - 45)

		check = True
		if len(nodes_set) != 0:
			for e_x, e_y in nodes_set:
				if abs(e_x - x) < 120 and abs(e_y - y) < 120: # create distance between nodes
					check = False
					break

		if check:
			nodes_set.append((x, y))
			node = Node(x, y, len(nodes_set))
			grid.append(node)

	return grid


# Draw to the screen
def draw(win, grid, width, components, components_font, lineConfig=(0, 0, 0, 0)):
	win.fill(WHITE)

	# Draw the line while dragging
	s_x, s_y, e_x, e_y = lineConfig
	if s_x != 0:
		pygame.draw.line(win, GREY, (s_x, s_y), (e_x, e_y), 5)

	# Print result to the screen
	if components != 0:
		text = components_font.render("There are " + str(components) + " components!", 1, BLACK)
		win.blit(text, (290, 10))


	for node in grid:
		for neighbour in node.neighbours:
			s_x, s_y = node.getCenterPosition()
			e_x, e_y = neighbour.getCenterPosition()
			pygame.draw.line(win, BLACK, (s_x, s_y), (e_x, e_y), 5)

	for node in grid:
		node.draw(win)
	pygame.display.update()


# ========================== Breadth First Search Algorithm ========================== #
def algorithm(draw, grid):
	colors = [RED, GREEN, TURQUOISE, ORANGE, BLUE, LIGHTGREEN, PURPLE, BROWN, LIGHTPURPLE, YELLOW]
	nodes = len(grid)
	count = 0
	visited = [False] * (nodes + 1)

	def dfs(nodeAt):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
		draw()
		time.sleep(0.4) 

		nonlocal visited, grid, count, colors
		visited[nodeAt] = True
		node = grid[nodeAt - 1]
		node.color = colors[count - 1]
		for nei in node.neighbours:
			if not visited[nei.order]:
				dfs(nei.order)


	for node in range(1, nodes + 1):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
		if not visited[node]:
			time.sleep(0.2)
			count += 1
			dfs(node)
	return count





def main(win, width):
	NODES = 10
	run = True
	grid = makeGrid(NODES, width)
	s_x = s_y = e_x = e_y = 0
	components = 0
	components_font = pygame.font.SysFont('comicsans', 30, True)

	startedAl = False
	while run:
		draw(win, grid, width, components, components_font, (s_x, s_y, e_x, e_y))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if not startedAl: # check if the algorithm started

				## Check for dragging ##
				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						mouse_x, mouse_y = event.pos
						for node in grid:
							if node.isAbove((mouse_x, mouse_y)):
								node.dragging = True
								node.makeDragged()

				elif event.type == pygame.MOUSEBUTTONUP: 
					if event.button == 1:
						mouse_x, mouse_y = event.pos
						for node in grid:
							if node.dragging:
								node.dragging = False
								s_x = s_y = e_x = e_y = 0
								node.reset()
								for node2 in grid:
									if node2 != node and node2.isAbove((mouse_x, mouse_y)) and node2 not in node.neighbours:
										node.neighbours.append(node2)
										node2.neighbours.append(node)

				elif event.type == pygame.MOUSEMOTION:
					for node in grid:
							if node.dragging:
								s_x, s_y = node.clickedPosition
								e_x, e_y = event.pos
				##------------------------##

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE: # Press Space to begin the al
						components = algorithm(lambda: draw(win, grid, width, components, components_font), grid)
						startedAl = True

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c: # Press C to restart
					for node in grid:
						components = 0
						node.reset()
						node.neighbours = []
						startedAl = False
							
	pygame.quit()

main(WIN, WIDTH)





















