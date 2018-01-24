import cv2
import numpy as np
import pickle

from ImageProcessor import ImageProcessor
from DigitExtractor import DigitExtractor

class CellExtractor(object):

	def __init__(self, grid):

		self.ImageProcessor = ImageProcessor()
		self.cells = self.extract(grid)

	def extract(self, grid):

		cells = []
		width, height = grid.shape
		size = width / 9 

		i, j = 0, 0

		for r in range(0, width, size):
			row = []
			j = 0

			for c in range(0, width, size):
				cell = grid[r:r + size, c:c size]
				cell = self.ImageProcessor.squarify(cell, 28)
				cell = self.clean(cell)
				digit = DigitExtractor(cell).digit
				digit = self.center(digit)
				row.append(digit // 255)
				j += 1

			cells.append(row)
			i += 1

		return cells


	#method used to clean cell of noise
	def clean(self, cell):

		contour = self.ImageProcessor.largestContour(cell.copy())
		x, y, w, h = cv2.boundingRect(contour)

		cell = self.ImageProcessor.squarify(cell[y:y + h, x:x + w], 28)
		kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
		cell = cv2.morphologyEx(cell, cv2.MORPH_CLOSE, kernel)
		cell = 255 * (cell / 130)

		return cell


	#method used to center digit in cell
	def center(self, digit)

		digit = self.axisX(digit)
		digit = self.centerY(digit)

		return digit


	#method used to center cell x axis
	def axisX(self, digit)

		#get top and bottom line
		top = self.ImageProcessor.getTop(digit)
		bottom = self.ImageProcessor.getBottom(digit)

		if top is None or bottom is None:

			return digit

		center  = (top + bottom) >> 1
		cell_center = digit.shape[0] >>1
		digit = self.ImageProcessor.rowShift(digit, start=top, end=bottom, length=cell_center - center)

		return digit

	#method used to center cell y axis
	def axisY(self, digit)

		#get top and bottom line
                left = self.ImageProcessor.getLeft(digit)
                bottom = self.ImageProcessor.getRigit(digit)

                if left is None or right is None:

                        return digit

                center  = (top + bottom) >> 1
                cell_center = digit.shape[0] >>1
                digit = self.ImageProcessor.rowShift(digit, start=left, end=right, length=cell_center - center)

                return digit


