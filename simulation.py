import pygame
import sys
import random
import time

from organism import Organism
from organism import Plant


class Simulation:
    window_width = 800
    window_height = 800

    def __init__(self):
        self.game_over = False
        self.population = []
        self.vegetation = []
        self.vegetation_rate = 30
        self.population_size = 30
        self.timer = 0
        self.paused = False

    def start_game(self):
        pygame.init()

        display = pygame.display.set_mode((Simulation.window_width, Simulation.window_height))

        pygame.display.set_caption('Natural Selection Simulation')

        self.populate()

        while not self.game_over:
            display.fill((255, 255, 255))

            # listen for events
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    result = self.get_organism(pos)
                    if result is not None:
                        print(result)
                    else:
                        new_organism = Organism(pos[0], pos[1])
                        new_organism.randomize()
                        self.population.append(new_organism)
                elif keys[pygame.K_SPACE]:
                    self.paused = not self.paused

            if not self.paused:
                self.tick()
                self.vegetate()
            self.draw(display)

            pygame.display.flip()

    def tick(self):
        for organism in self.population:
            organism.get_older(self.population)
            organism.perceive(self.population + self.vegetation)
            organism.decide()
            organism.act()
            organism.move(self.window_width, self.window_height)

    def vegetate(self):
        # grow a new plant
        if random.uniform(0, 100) < 3:
            pos = (int(random.uniform(0, Simulation.window_width - 5)), int(random.uniform(0, Simulation.window_height - 5)))
            plant = Plant(pygame.Rect(pos[0], pos[1], 6, 6))
            self.vegetation.append(plant)

        # check whether or not the plant was eaten and grow over time
        for plant in self.vegetation:
            eaten = self.eat_plant(plant)
            if not eaten:
                if plant.bounds.width < 10 and random.uniform(0, 100) < 1:
                    plant.bounds.width += 1
                    plant.bounds.height += 1

    def draw(self, display):
        for organism in self.population + self.vegetation:
            organism.draw(display)

    def populate(self):
        for i in range(self.population_size):
            organism = Organism()
            organism.randomize()
            self.population.append(organism)

    def get_organism(self, pos):
        for organism in self.population:
            if organism.bounds.collidepoint(pos):
                return organism

    def eat_plant(self, plant):
        for organism in self.population:
            if organism.bounds.colliderect(plant.bounds):
                organism.eating = True
                organism.hungry = False
                organism.hunger = None
                organism.ate = time.time()
                organism.food_eaten += 1
                organism.lifetime += (20 / organism.food_eaten)
                organism.endurance += (1 / organism.food_eaten)
                if organism.food_eaten % 5 == 0:
                    organism.bounds.inflate_ip(2, 2)
                self.vegetation.remove(plant)
                organism.target = None
                return True

    def eat_prey(self, prey):
        pass


if __name__ == '__main__':
    simulation = Simulation()
    simulation.start_game()