import pygame
import random
import math

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
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Node:
	def __init__(self, x, y, order):
		self.x = x
		self.y = y
		self.order = order
		self.radius = 40
		self.borderWidth = 5
		self.color = BLACK
		self.edges = []
		self.neighbours = []
		self.dragging = False
		self.clickedPosition = ()

	def isCliked(self, point):
		p_x, p_y = point
		self.clickedPosition = (p_x, p_y)
		distance = math.sqrt((self.x - p_x) * (self.x - p_x) + (self.y - p_y) * (self.y - p_y))

		return distance <= self.radius

	def getCenterPosition(self):
		return self.x, self.y

	def draw(self, win):
		win.blit(nodesImages[self.order - 1], (self.x - 45, self.y - 40))
		pygame.draw.circle(win, self.color, (self.x, self.y), self.radius, self.borderWidth)

	def __str__(self):
		return self.order

	def reset(self):
		self.color = BLACK

	def makeDragged(self):
		self.color = GREEN



def makeGrid(nodes, width):
	grid = []
	nodes_set = []

	while len(nodes_set) < nodes:
		x = random.randint(45, 760)
		y = random.randint(45, 760)

		check = True
		if len(nodes_set) != 0:
			for e_x, e_y in nodes_set:
				if abs(e_x - x) < 90 and abs(e_y - y) < 90:
					check = False
					break

		if check:
			nodes_set.append((x, y))
			node = Node(x, y, len(nodes_set))
			grid.append(node)
			print(node.order)

	return grid


def draw(win, grid, nodes, width, lineConfig):
	win.fill(WHITE)
	s_x, s_y, e_x, e_y = lineConfig

	if s_x != 0:
		pygame.draw.line(win, GREY, (s_x, s_y), (e_x, e_y), 5)

	for node in grid:
		node.draw(win)
	pygame.display.update()




def main(win, width):
	NODES = 10
	run = True
	grid = makeGrid(NODES, width)
	s_x = s_y = e_x = e_y = 0

	while run:
		draw(win, grid, NODES, width, (s_x, s_y, e_x, e_y))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					mouse_x, mouse_y = event.pos
					for node in grid:
						if node.isCliked((mouse_x, mouse_y)):
							node.dragging = True
							node.makeDragged()
			elif event.type == pygame.MOUSEBUTTONUP: 
				if event.button == 1:
					for node in grid:
						if node.dragging:
							node.dragging = False
							s_x = s_y = e_x = e_y = 0
							node.reset()
			elif event.type == pygame.MOUSEMOTION:
				for node in grid:
						if node.dragging:
							s_x, s_y = node.clickedPosition
							e_x, e_y = event.pos
							
	pygame.quit()

main(WIN, WIDTH)





















