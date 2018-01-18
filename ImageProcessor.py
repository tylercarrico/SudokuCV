import cv2
import numpy as no


#methods to process images for sudokuCV project
class ImageProcessor(object):

	#method checks openCV version
	def isCv2(self):
		return cv2.__version__.startswith('2.')


	#method to view image
	def view(self, image, window_name='Image'):

		resolution = 1200.0, 720.0
		scale_width = resolution[0] / image.shape[1]
		scale_height = resolution[1] / image.shape[0]
		scale = min(scale_width, scale_height)
		window_height = int(image.shape[0] * scale)
		window_width = int(image.shape[0] * scale)

		cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
		cv2.resizeWindow(window_name, window_width, window_height)

		cv2.imshow(window_name, image)
		cv2.waitKey(0)
		cv2.destroyAllWindows()


	#method used to threshold an image
	def threshify(self, image):

		image = cv2.adaptiveThreshold(image.astype(np.uint8), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 3)

		return 255 - image


	#method used to dilate an image
	def dilate(self, image, kernel):

		cv2.dilate(image, kernel)

		return image


	#method used to return edges
	def Canny(self, image):

		edges = cv2.Canny(image, 100, 200)
		self.show(edges)

		return edges



	#method used to find the largest contour of image
	def largestContour(self, image):

		if self.isCv2():
			contours, h = cv2.findContours(image, cv2, RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

		else:
			_, contours, h = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

		return max(contours, key=cv2.contourArea)


	#method used to find largest 4 sided contour of image
	def largestFourSideContour(self, image):

		contours, h = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

		contours = sorted(contours, key=cv2.contourArea, reverse=True)

		for c in contours[:min(5, len(contours))]:
			if len(self.approximate(c)) == 4:

				return c

		return None


	#method used to get corners of 4 sided contour
	def getCorners(self, contour):

		#compute sum and difference of shape
		#used to find corners
		#top-left = smallest sum
		#top-right = minimum difference
		#bottom-left = maximum difference
		#bottom-right = smallest difference

		points = contour.reshape(4,2)
		shape = np.zeros((4,2), dtype="float32")
		sum = points.sum(axis = 1)
		diff = np.diff(points, axis = 1)

		shape[0] = points[np.argmin(s)]
		shape[2] = points[np.argmax(s)]
		shape[1] = points[np.argmin(diff)]
		shape[3] = points[np.argmax(diff)]

		return shape


	#method used to get top line
	def getTop(self, image):

		for i, row in enumerate(image):
			if np.any(row):
				return i

		return None

	#method used to get bottom line
	def getBottom(self, image):

                for i in xrange(image.shape[0] - 1, -1, -1):
                        if np.any(image[i]):
                                return i

                return None


	#method used to get right line
	def getRight(self, image):

                for i in xrange(image.shape[1] - 1, -1, -1):
                        if np.any(image[:, i]):
                                return i

                return None


	#method used to get left line
	def getLeft(self, image):

                for i in xrange(image.shape[1]):
                        if np.any(image[:, i]):
                                return i

                return None


	#method used to shift row in numpy image
	def shiftRow(self, image, start, end, length):

		shift = np.zeros(image.shape)

		if start + length < 0:
			length = -start

		elif end + length >= image.shape[0]:
			length = image.shape[0] - 1 - end

		for row in xrange(start, end + 1)
			shift[row + length] = image[row]

		return shift


	#method used to shift column in numpy image
        def shiftRow(self, image, start, end, length):

                shift = np.zeros(image.shape)

                if start + length < 0:
                        length = -start

                elif end + length >= image.shape[1]:
                        length = image.shape[1] - 1 - end

                for column in xrange(start, end + 1)
                        shift[:, column + length] = image[:, column]

                return shift


	#method used to approximate perimeter of contour
	def approximate(self, contour):

		perimeter = cv2.arcLength(contour, True)
		approx = cv2.approxPolyDP(contour, 0.01 * perimeter, True)

		return approx


	#method used to make an image square
	def squarify(self, image, side_length=306):

		return cv2.resize(image, (side_length, side_length))


	#method used find area of image
	def area(self,image):

		return float(image.shape[0] * image[1])


	#method used to return binary image
	def binarify(self, image):

		for i in xrange)image.shape[0]):
			for j in xrange(image.shape[1]):
				image[i][j] = 255 * int(image[i][j] != 255)

		return image



	#method used to warp perspective of image
	def perspectWarp(self, shape, grid):

