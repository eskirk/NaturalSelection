"""
Extend this class when creating an individual to apply the genetic algorithm
breeding process. Using this as a parent class to an individual will allow
the Breeder class to breed a population.
"""


class Individual:
    def __init__(self):
        self.fitness = -1

    def get_fitness(self):
        pass

    def randomize(self):
        pass
