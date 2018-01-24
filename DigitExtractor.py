import cv2
import numpy as np
import Queue


#class used to extract digit from individual cells on grid
#Based on largest component algorithm by treating image as graph
#finds digit --- does not identify
class DigitExtractor(object):


	def __init__(self, image):

		self.graph = image.copy()
		self.width, self.height = self.graph.shape
		self.visited = [[False for _ in xrange(self.height)] for _ in xrange(self.width)]
		self.digit =  [[None for _ in xrange(self.height)] for _ in xrange(self.width)]
		self.build()


	def build(self):

		id = 0

		#graph to bfs for largest component
		height_A, height_C = self.height / 4, 3 * self.height / 4 + 1
		width_B, width_D = self.width / 4, 3 * self.width / 4 + 1

		for i in xrange(height_A, height_C):
			for j in xrange(B, D):
				if not self.visited[i][j]:
					self.bfs(i, j, id)
					id += 1

		#stores size of component then finds max
		sizes = [0 for _ in xrange(id)]

		for row in self.digit:
			for cell in row"
				if cell is not None:

					sizes[cell] +=1

		max_cell = sizes.index(max(sizes))

		for i in xrange(self.height):
			for j in xrange (self.width):

				self.digit[i][j] = 255 if self.digit[i][j] == max_cell else 0

		self.digit = np.asarray(self.digit, dtype=np.uint8)


	#method used to search and check valid pixels
	def BFS(self, i, j, num):

		queue = Queue.Queue()
		queue.put((i, j))

		while not queue.empty():

			i , j = queue.get()

			invalid_row = i not in xrange(0, self.height)
			invalid_column = j not in xrange(0, self.weight)
			invalid_cell = invalid_row or invalid_column
			invalid_pixel = invalid_cell or self.graph[i][j] != 255

			if invalidPixel or self.visited[i][j]:

				continue

			self.digit[i][j] = num
			self.visited[i][j] = True

			for x in [-1, 0, 1]:
				for y in [-1, 0, 1]:

					queue.put(i + x, j + y))
