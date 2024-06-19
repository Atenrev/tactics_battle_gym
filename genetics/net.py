import numpy as np

from .matrix import Matrix


class Net:

    def __init__(self, input_nodes, hidden_nodes, output_nodes):
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes

        self.ih_weights = Matrix(hidden_nodes, input_nodes+1)
        self.hh_weights = Matrix(hidden_nodes, hidden_nodes+1)
        self.ho_weights = Matrix(output_nodes, hidden_nodes+1)

        self.ih_weights.randomize()
        self.hh_weights.randomize()
        self.ho_weights.randomize()

        self.fitness = 0.0

    def load(self, file_path):
        weights = np.load(file_path, allow_pickle=True)
        self.ih_weights.matrix = weights[0]
        self.hh_weights.matrix = weights[1]
        self.ho_weights.matrix = weights[2]

    def save(self, file_path):
        np.save(file_path, [self.ih_weights.matrix,
                self.hh_weights.matrix, self.ho_weights.matrix])

    def forward(self, inputs):
        X = Matrix.column_matrix_from_array(inputs)
        X = X.add_bias()

        # Calculate the first layer
        X = self.ih_weights.multiply_by_matrix(X)
        X = X.activate()
        X = X.add_bias()

        # Calculate the second layer
        X = self.hh_weights.multiply_by_matrix(X)
        X = X.activate()
        X = X.add_bias()

        # Calculate the outputs
        X = self.ho_weights.multiply_by_matrix(X)

        return X.to_array()

    def mutate(self, mutation_rate):
        self.ih_weights.mutate(mutation_rate)
        self.hh_weights.mutate(mutation_rate)
        self.ho_weights.mutate(mutation_rate)

    def crossover(self, other, crossover_rate):
        c = Net(self.input_nodes, self.hidden_nodes, self.output_nodes)
        c.ih_weights = self.ih_weights.crossover(
            other.ih_weights, crossover_rate)
        c.hh_weights = self.hh_weights.crossover(
            other.hh_weights, crossover_rate)
        c.ho_weights = self.ho_weights.crossover(
            other.ho_weights, crossover_rate)
        return c

    def clone(self):
        c = Net(self.input_nodes, self.hidden_nodes, self.output_nodes)
        c.ih_weights = self.ih_weights.clone()
        c.hh_weights = self.hh_weights.clone()
        c.ho_weights = self.ho_weights.clone()
        return c


if __name__ == "__main__":
    e = Net(64, 32, 9)
    e.mutate(0.1)
    print(e.forward([i for i in range(64)]))
