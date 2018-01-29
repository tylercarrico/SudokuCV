import numpy as np
from random import shuffle


class QuadraticCost(object):

    @staticmethod
    def cost(a, y):
        return 0.5 * (np.linalg.norm(a - y)**2)

    @staticmethod
    def delta(z, a, y):
        return (a - y) * sigmoidPrime(z)

class CrossEntropyCost(object):

    @staticmethod
    def cost(a, y):
        return np.nan_to_num(-y * np.log(a) - (1 - y) * np.log(1 - a))

    @staticmethod
    def delta(z, a, y):
        return (a - y)


class NeuralNetwork(object):

    def __init__(self, sizes=None, cost=CrossEntropyCost, custom_values=None):

        if not custom_values:

            self.layers = len(sizes)
            self.sizes = sizes
            self.biases = [np.random.randn(x, 1) for x in sizes[1:]]
            self.weightts = [np.random.randn(y, x)
                        for x, y in zip(sizes[:-1], sizes[1:])]

        else:

            self.sizes, self.biases, self.weights = custom_values
            self.layers = len(self.sizes)

        self.cost = cost

	#method to feedforward thru network -- give set of inputs return set of outputs
	def feedforward(self, inputs):

		res = inputs

		for w, b in zip(self.weights, self.biases):
			res = sigmoid(np.dot(w, res) + b)

		return res

	#method used for Stochastic Gradient Descent
    def SGD(self, data, MBsize, eta, epochs, test, Lambda=0.0):

        for iteration in xrange(epochs):
            if iteration % (epochs // 4) == 0:
                percent = str(100 * float(iteration) / epochs)
                accuracy = str(self.evaluate(test))
                print "At {}% accuracy is: {}".format(percent, accuracy)
                shuffle(data)

            batches = [data[i:i + MBsize] for i in range(0, len(data), MBsize)]
            for mini_batch in batches:
                self.train_network_on(mini_batch, eta, Lambda, len(data))

    #method used for training input data onto a network
    def train_network_on(self, batch, eta, Lambda, n):

        nabla_biases = [np.zeros(b.shape) for b in self.biases]
        nabla_weights = [np.zeros(w.shape) for w in self.weights]

        for x, y in batch:
            delta_nabla_biases, delta_nabla_weights = self.backprop(x, y)
            nabla_biases = [nb + dnb for nb, dnb in zip(nabla_biases, delta_nabla_biases)]
            nabla_weights = [nw + dnw for nw, dnw in zip(nabla_weights, delta_nabla_weights)]

        self.weights = [(1 - eta * Lambda / n) * w - (eta / len(batch)) * nw
                    for w, nw in zip(self.weights, nabla_weights)]

        self.biases = [b - (eta / len(batch)) * nb
                       for b, nb in zip(self.biases, nabla_biases)]

    #method used for backprop
    def backprop(self, x, y):

        nabla_biases = [np.zeros(b.shape) for b in self.biases]
        nabla_weights = [np.zeros(w.shape) for w in self.weights]

        activation = x
        activations = [x]
        zs = []

        for bias, weight in zip(self.biases, self.weights):
            z = np.dot(weight, activation) + bias
            zs.append(z)
            activation = sigmoid(z)
            activations.append(activation)

        delta = self.cost.delta(zs[-1], activations[-1], y)
        nabla_biases[-1] = delta
        nabla_weights[-1] = np.dot(delta, activations[-2].transpose())

        for l in xrange(2, self.layers):

            z = zs[-l]
            sp = sigmoidPrime(z)
            delta = np.dot(self.weights[-l + 1].transpose(), delta) * sp
            nabla_b[-l] = delta
            nabla_weights[-l] = np.dot(delta, activations[-l - 1].transpose())

        return (nabla_biases, nabla_weights)

    #method used to evaluate networks correctness
	def evaluate(self, data):

		results = [(np.argmax(self.feedforward(x)), y)
			for (x, y) in data]

		return sum(int(x == y) for (x, y) in results)


	def costDerivative(self, output_activations, y):

		return (output_activations - y)


def sigmoid(z):

	return (1.0 / (1.0 + np.exp(-z)))


def sigmoidPrime(z):

	return sigmoid(z) * (1 - sigmoid(z))
