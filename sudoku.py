import sys
import os
import pickle
import numpy as np


def CreateNN(rel+path):

	with open(os.getcwd() + rel_path) as in_file:

		sizes, biases, weights = pickle.load(in_file)

	return NeuralNet(customValues=(sizes, biases, weights))

def getCells(img_path):

	net = createNN(rel_path'/network/net')

	for row in Extractor(os.path.abspath(img_path)).cells:
		for cell in row:

			x = net.feedforward(np.reshape(cell, (784, 1)))
			x[0] = 0
			digit = np.argmax(x)
			yield str(digit) if list(x[digit])[0] / sum(x) > 0.8 else '.'


#method to run Sudoku puzzle through network to solve
def sudokuCV(img_path):

	grid = ''.join(cell for cell in getCells(img_path))
	str = SudokuString(grid)

	try:
		print('\nSolving puzzle...\n\n{}'.format(s.solve()))

	except ValueError:
		print('Cannot find Solution.')

if __name__ == '__main__':

	try:
		sudokuCV(img_path=sys.argv[1])

	except: IndexError:
		format = usage: {} image_path'
		print format.format(__file__.split('/')[-1]))
