import numpy as np

from .activations import v_relu, v_sigmoid


class Matrix:

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.matrix = np.zeros((rows, columns))

    @staticmethod
    def from_1d_array(rows, columns, array) -> 'Matrix':
        m = Matrix(rows, columns)

        for i in range(rows):
            for j in range(columns):
                m.matrix[i][j] = array[i*columns+j]

        return m

    @staticmethod
    def column_matrix_from_array(array) -> 'Matrix':
        m = Matrix(len(array), 1)

        for i in range(len(array)):
            m.matrix[i][0] = array[i]

        return m

    def multiply_by_matrix(self, m) -> 'Matrix':
        if self.columns != m.rows:
            raise Exception("Matrices don't match")

        n = Matrix(self.rows, m.columns)
        n.matrix = np.dot(self.matrix, m.matrix)
        return n

    def randomize(self):
        for i in range(self.rows):
            for j in range(self.columns):
                self.matrix[i][j] = np.random.normal()

                if self.matrix[i][j] > 1.0:
                    self.matrix[i][j] = 1.0
                elif self.matrix[i][j] < -1.0:
                    self.matrix[i][j] = -1.0

    def add_bias(self) -> 'Matrix':
        m = Matrix(self.rows+1, 1)

        for i in range(self.rows):
            m.matrix[i][0] = self.matrix[i][0]
        
        m.matrix[self.rows][0] = 1
        self.rows += 1
        return m

    def activate(self) -> 'Matrix':
        m = Matrix(self.rows, self.columns)
        m.matrix = v_sigmoid(self.matrix)
        return m

    def crossover(self, other, crossover_rate):
        c = self.clone()

        for i in range(self.rows):
            for j in range(self.columns):
                if np.random.random() < crossover_rate:
                    c.matrix[i][j] = other.matrix[i][j]

        return c

    def mutate(self, mutation_rate):
        for i in range(self.rows):
            for j in range(self.columns):
                if np.random.random() < mutation_rate:
                    self.matrix[i][j] += np.random.normal() / 5.0

                    if self.matrix[i][j] > 1.0:
                        self.matrix[i][j] = 1.0
                    elif self.matrix[i][j] < -1.0:
                        self.matrix[i][j] = -1.0

    def clone(self):
        c = Matrix(self.rows,self.columns)
        c.matrix = self.matrix.copy()
        return c

    def to_array(self):
        arr = []

        for i in range(self.rows):
            for j in range(self.columns):
                arr.append(self.matrix[i][j])
                
        return arr
    
    def print(self):
        for i in range(self.rows):
            print(self.matrix[i])   