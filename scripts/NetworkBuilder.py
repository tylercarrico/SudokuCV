import os
import pickle
import numpy as np

from GridExtractor import GridExtractor


def load(filename):
    with open(filename) as in_file:
        return pickle.load(in_file)

def dump(data, filename):
    with open(filename, 'w') as out_file:
        pickle.dump(data, out_file)


class Builder(object):
    '''
    Builds dataset from images in a folder.
    '''

    def __init__(self, img_dir=None, rebuild=False):

        self.img_dir = (os.path.abspath(img_dir) if img_dir else os.path.join(os.path.dirname(os.getcwd()), 'train/'))
        self.usedSet = {}

        if rebuild == False:
            usedSetPath = os.path.join(os.getcwd(), 'usedSet')
            if os.path.exists(usedSetPath):
                self.usedSet = load(usedSetPath)

        self.training_data = load('train') if self.usedSet else []
        self.testing_data = load('test') if self.usedSet else []

        try:
            for img_path, results, file in self.getUnused():
                cells = GridExtractor(img_path).cells
		print cells
                trainingInputs = [[np.reshape(cell, (784, 1)) for cell in row] for row in cells]
                trainingResults = [[self.vectorify(int(digit)) for digit in row] for row in results]
                for i in xrange(9):
                    for j in xrange(9):
                        if trainingResults[i][j] is None:
                            continue
                        self.training_data.append(
                            (trainingInputs[i][j], trainingResults[i][j]))
                        self.testing_data.append(
                            (trainingInputs[i][j], int(results[i][j])))
                self.usedSet[file] = True

        except:
            self.save()
            raise
        self.save()

    def getUnused(self):
        for file in os.listdir(self.img_dir):
            if file.endswith('.jpg') and file not in self.usedSet:
                image_path = os.path.join(self.img_dir, file)
                result_path = os.path.join(self.img_dir, file[:-3] + 'dat')
                results = None

                try:
                    with open(result_path, 'r') as resFile:
                        results = [list(row) for row in resFile.read().splitlines()]

                except IOError:
                    continue
                yield (image_path, results, file)

    def vectorify(self, j):
        if j == 0:
            return None
        e = np.zeros((10, 1))
        e[j] = 1.0
        return e

    def save(self):
        dump(self.usedSet, 'usedSet')
        dump(self.training_data, 'train')
        dump(self.testing_data, 'test')

Builder()
