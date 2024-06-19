import numpy as np

from typing import Tuple
from .net import Net


class GeneticManager:
    """
    Class that implements a genetic algorithm 
    and manages the current instances of the nets.
    """
    instance: 'GeneticManager' = None

    def __init__(self,
                 population_size: int,
                 mutation_rate: float,
                 crossover_rate: float,
                 net_params: dict,
                 ):
        """
        Initializes the genetic manager.
        :param population_size: The size of the population.
        :param mutation_rate: The rate of mutation.
        :param crossover_rate: The rate of crossover.
        :param max_generations: The maximum number of generations.
        :param max_fitness: The maximum fitness.
        :param net_manager: The net manager.
        """
        self.population_size = population_size
        self.population = []
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.net_params = net_params
        self.current_generation = 0
        self.best_fitness = 0
        self.current_fitness = 0
        self.iteration = 0

    @classmethod
    def set_instance(cls, instance: 'GeneticManager'):
        """
        Sets the instance of the genetic manager.
        :param instance: The instance of the genetic manager.
        """
        cls.instance = instance

    @classmethod
    def get_instance(cls) -> 'GeneticManager':
        """
        Returns the singleton instance of the genetic manager.
        """
        return cls.instance

    def initialize_population(self):
        """
        Initializes the population.
        """
        for _ in range(self.population_size):
            self.population.append(Net(**self.net_params))

    def get_best_net(self) -> Tuple[int, Net]:
        """
        Returns the best net.
        :return: The best net and its index.
        """
        best_net = self.population[0]
        best_net_index = 0
        
        for i, net in enumerate(self.population):
            if net.fitness > best_net.fitness:
                best_net = net
                best_net_index = i

        return best_net_index, best_net

    def next_iteration(self):
        """
        Performs the next iteration.
        """
        self.iteration += 1

    def get_current_net(self) -> Net:
        """
        Returns the current net.
        :return: The current net.
        """
        return self.population[self.iteration]

    def new_generation(self):
        """
        Starts a new generation.
        """
        self.current_generation += 1
        self.current_fitness = self.get_average_fitness()
        self.iteration = 0
        self.natural_selection()

    def natural_selection(self):
        """
        Performs natural selection.
        """
        self.population.sort(key=lambda net: net.fitness, reverse=True)

        # best_net_array = best_net.to_array()
        # best_net_array.dump('best_net.npy')
        # best_net.save_to_file(f"best_net_{self.current_generation}.csv")

        # Save the best net to a file.
        self.population[0].save(f"models/best_net_{self.current_generation}.npy")
        self.best_fitness = self.population[0].fitness

        # Remove the worst 60% of the population.
        self.population = [net.clone() for net in self.population[:int(self.population_size * 0.4)]]

        # Make 10% clones of the best net
        for _ in range(self.population_size // 2 - len(self.population)):
            self.population.append(self.population[0].clone())

        # Add crossover of the best half of the population
        self.crossover()

        # Mutate the population
        self.mutate()


    def crossover(self):
        """
        Performs crossover.
        """
        for i in range(self.population_size // 2):
            net1 = self.population[i]
            net2 = self.population[np.random.randint(self.population_size // 2)]
            new_net = net1.crossover(net2, self.crossover_rate)
            self.population.append(new_net)

    def mutate(self):
        """
        Performs mutation.
        """
        for net in self.population[1:self.population_size // 2]:
            net.mutate(self.mutation_rate)

    def get_current_iteration_fitness(self) -> float:
        """
        Returns the current fitness.
        :return: The current fitness.
        """
        return self.population[self.iteration].fitness

    def get_average_fitness(self) -> float:
        """
        Returns the average fitness.
        :return: The average fitness.
        """
        return sum(net.fitness for net in self.population) / self.population_size