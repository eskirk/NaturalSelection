"""
This class is used to breed a population of individuals inheriting the
Individual class.
Inherit the Breeder class and override the `breed` and `get_fit_individuals`
methods in a way that allows you to find the fit individuals and breed them
together.
Begin the breeding process with Breeder.start_breeding().
"""
from individual import Individual


class Breeder:
    # Initialize a new population
    def __init__(self, parent, population_size=50):
        self.population_size = population_size - (population_size % 2)
        self.population = []
        self.create_population(parent)

    # Breed two individuals together
    @staticmethod
    def breed(parent1, parent2):
        return parent1, parent2

    # Create a new random population from the parent
    def create_population(self, parent):
        for i in range(self.population_size):
            self.population.append(parent.randomize())

    # Return the fittest individuals of the population
    def get_fit_individuals(self):
        return self.population

    # Begin the breeding process after the fitness has been determined
    def start_breeding(self):
        for i in range(0, len(self.get_fit_individuals()), 2):
            self.breed(self.population[i], self.population[i + 1])
