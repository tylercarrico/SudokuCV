import pickle

from NNetworkTrain import NeuralNetwork

#used to load training and testing data into network
with open('train', 'r') as in_file:
    training = pickle.load(in_file)

with open('test', 'r') as in_file:
    testing = pickle.load(in_file)

network = NeuralNetwork([784, 30, 30, 10])
network.SGD(training, 1, 0.05, len(training), testing, 0.5)

with open('../scripts/network/net', 'w') as out_file:
    pickle.dump((network.sizes, network.biases, network.weights), out_file)
