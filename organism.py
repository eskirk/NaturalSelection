import pygame
import random
import math
import time


class Organism:
    def __init__(self, x_pos=None, y_pos=None):
        if x_pos is not None and y_pos is not None:
            self.bounds = pygame.Rect(x_pos, y_pos, 15, 15)
        else:
            self.bounds = pygame.Rect(random.uniform(20, 780), random.uniform(20, 780), 15, 15)
        self.color = (random.uniform(0, 255), random.uniform(0, 255), random.uniform(0, 255))
        self.birth = time.time()
        self.age = 0
        self.name = 'Organism ' + str(self.color)
        self.parents = None
        # attributes
        self.speed = 0
        self.strength = 0
        self.focus = 0
        self.perception = 0
        self.endurance = 0
        self.sociability = 0
        self.survivability = 0
        self.sex = None
        # stats
        self.food_eaten = 0
        self.lifetime = 0
        self.focus_time = 0
        self.fitness = 0
        self.generation = 0
        # status
        self.foraging = False
        self.reproducing = False
        self.herding = False
        self.fertile = False
        self.pregnant = False
        self.baby = None
        self.time_pregnant = 0
        self.eating = False
        self.target = None
        self.mouth = 0
        self.reproduced = time.time()
        # perceptions
        self.plant_perceptions = []
        self.organism_perceptions = []

    def __repr__(self):
        return '\nSpeed: ' + str(self.speed) + '\nStrength: ' + str(self.strength) + \
               '\nFocus: ' + str(self.focus) + '\nPerception: ' + str(self.perception) + \
               '\nEndurance: ' + str(self.endurance) + '\nSurvivability: ' + str(self.survivability) + \
               '\nSociability: ' + str(self.sociability) + '\nSex: ' + str(self.sex) + \
               '\nPlants Eaten: ' + str(self.food_eaten) + '\nPregnant: ' + str(self.pregnant) + \
               '\nHerding: ' + str(self.herding) + '\nReproducing: ' + str(self.reproducing) + \
               '\nForaging: ' + str(self.foraging) + '\nAge: ' + str(self.age) + \
               '\nLifetime: ' + str(self.lifetime) + '\nPerceptions: ' + str(self.plant_perceptions) + \
               '\nTarget: ' + str(self.target.__class__) + '\nGeneration: ' + str(self.generation)

    def draw(self, display):
        pygame.draw.rect(display, self.color, self.bounds)
        pygame.draw.circle(display, (255, 255, 255), (self.bounds.x + self.bounds.width / 4, self.bounds.y + 5), 3)
        pygame.draw.circle(display, (255, 255, 255), (self.bounds.x + self.bounds.width - 4, self.bounds.y + 5), 3)
        pygame.draw.circle(display, (0, 0, 0), (self.bounds.x + self.bounds.width / 4, self.bounds.y + 5), 1)
        pygame.draw.circle(display, (0, 0, 0), (self.bounds.x + self.bounds.width - 4, self.bounds.y + 5), 1)

        if not self.eating:
            pygame.draw.line(display, (255, 255, 255), (self.bounds.x + 3, self.bounds.y + self.bounds.height - 4),
                             (self.bounds.x + self.bounds.width - 3, self.bounds.y + self.bounds.height - 4), 1)
        else:
            pygame.draw.line(display, (255, 255, 255), (self.bounds.x + 3, self.bounds.y + self.bounds.height - 4),
                             (self.bounds.x + self.bounds.width - 3, self.bounds.y + self.bounds.height - 4),
                             self.mouth)
            if self.mouth < 5:
                if random.uniform(0, 1) < 0.2:
                    self.mouth += 1
            else:
                self.eating = False
                self.mouth = 1

    def move(self, width, height):
        if random.uniform(0, 50) <= 10:
            if self.target is None:
                delta_x, delta_y = self.move_randomly()
            else:
                delta_x, delta_y = self.move_towards_target()

            if self.bounds.width < (self.bounds.x + self.bounds.width) + delta_x < width \
                    and self.bounds.height < (self.bounds.y + self.bounds.height) + delta_y < height:
                self.bounds = self.bounds.move((delta_x, delta_y))

    def move_towards_target(self):
        if self.bounds.x < self.target.bounds.x:
            delta_x = random.uniform(self.speed / 10, self.speed / 2)
            if self.bounds.y < self.target.bounds.y:
                delta_y = random.uniform(self.speed / 10, self.speed / 2)
            elif self.bounds.y > self.target.bounds.y:
                delta_y = random.uniform(-self.speed / 2, -self.speed / 10)
            else:
                delta_y = 0
        elif self.bounds.x > self.target.bounds.x:
            delta_x = random.uniform(-self.speed / 2, -self.speed / 10)
            if self.bounds.y < self.target.bounds.y:
                delta_y = random.uniform(self.speed / 10, self.speed / 2)
            elif self.bounds.y > self.target.bounds.y:
                delta_y = random.uniform(-self.speed / 2, -self.speed / 10)
            else:
                delta_y = 0
        elif self.bounds.x == self.target.bounds.x and self.bounds.y == self.target.bounds.y:
            delta_x, delta_y = self.move_randomly()
        else:
            delta_x = 0
            if self.bounds.y < self.target.bounds.y:
                delta_y = random.uniform(self.speed / 10, self.speed / 2)
            elif self.bounds.y > self.target.bounds.y:
                delta_y = random.uniform(-self.speed / 2, -self.speed / 10)
            else:
                delta_y = 0
        return delta_x, delta_y

    def move_randomly(self):
        delta_x = random.uniform((-self.speed / 2), self.speed / 2)
        delta_y = random.uniform((-self.speed / 2), self.speed / 2)
        return delta_x, delta_y

    def get_older(self, population):
        self.age = time.time() - self.birth

        if self.age > self.lifetime:
            self.die(population)
        elif not self.fertile and self.lifetime <= self.age / 4 <= self.lifetime / 3:
            self.fertile = True
        elif not self.fertile and time.time() - self.reproduced >= self.lifetime / ((self.endurance / 50) * 5):
            self.fertile = True

        if self.pregnant:
            if time.time() - self.time_pregnant > self.lifetime / 10:
                self.baby.bounds.x, self.baby.bounds.y = self.bounds.x, self.bounds.y
                population.append(self.baby)
                print('Birth, population: ', len(population))
                self.fertile = False
                self.pregnant = False
                self.baby = None
                self.time_pregnant = 0

    def die(self, population):
        if self.bounds.width > 0 and random.uniform(0, 100) < 10:
            self.speed = self.speed / 2
            self.focus = self.focus / 2
            self.bounds.width -= 1
            self.bounds.height -= 1
        elif self.bounds.width == 0:
            population.remove(self)
            print('Death, population: ', len(population))

    def randomize(self):
        speed = random.uniform(0, 1)
        strength = random.uniform(0, 1)
        perception = random.uniform(0, 1)
        focus = random.uniform(0, 1)
        endurance = random.uniform(0, 1)
        total = speed + strength + perception + focus + endurance

        self.sociability = random.uniform(0, 1)
        self.survivability = 1 - self.sociability
        self.sex = random.choice(['M', 'F'])
        self.speed = (speed / total) * 100
        self.strength = (strength / total) * 100
        self.focus = (focus / total) * 100
        self.perception = (perception / total) * 100
        self.endurance = (endurance / total) * 100
        self.lifetime = (self.strength + self.endurance) * 3

    def perceive(self, population):
        self.plant_perceptions = []
        self.organism_perceptions = []
        for organism in population:
            if self.get_dist(organism) <= self.perception * 5:
                if organism.__class__ == Plant and organism not in self.plant_perceptions:
                    self.plant_perceptions.append(organism)
                elif organism.__class__ == Organism and organism not in self.organism_perceptions:
                    self.organism_perceptions.append(organism)

    def decide(self):
        if self.target is None or time.time() - self.focus_time > self.focus:
            if self.fertile and not self.pregnant and random.uniform(0, 50) < self.endurance:
                self.find_mate()
            elif len(self.plant_perceptions) > 1 and random.uniform(0, 5) < self.survivability:
                self.find_food()
            elif len(self.organism_perceptions) > 1 and random.uniform(0, 5) < self.sociability:
                self.find_herd()
            else:
                self.target = None

    def act(self):
        if self.herding:
            self.herd()
        elif self.reproducing and self.fertile:
            self.mate()
        elif self.foraging:
            pass

    def find_food(self):
        if len(self.plant_perceptions) > 0:
            self.foraging = True
            self.reproducing = False
            self.herding = False
            self.focus_time = time.time()
            self.target = random.choice(self.plant_perceptions)
        else:
            self.foraging = False
            self.reproducing = False
            self.herding = False
            self.target = None

    def find_mate(self):
        self.foraging = False
        self.herding = False
        if len(self.organism_perceptions) > 0:
            self.focus_time = time.time()
            self.target = random.choice(self.organism_perceptions)
            self.reproducing = True
            if self.sex == 'M' and self.target.sex != 'F':
                self.target = None
                self.reproducing = False
            elif self.sex == 'F' and self.target.sex != 'M':
                self.target = None
                self.reproducing = False
        else:
            self.target = None
            self.reproducing = False

    def mate(self):
        if self.target is not None and self.target and self.bounds.colliderect(self.target.bounds):
            self.fertile = False
            if self.sex == 'F' and not self.pregnant and self.target.fertile:
                self.reproducing = False
                self.reproduced = time.time()
                if self.target.fertile and random.uniform(0, 100) < self.endurance:
                    self.pregnant = True
                    self.fitness += 1
                    self.target.fitness += 1
                    self.make_baby(self.target)
                self.target = None
            elif self.sex == 'M' and self.target.fertile:
                self.reproducing = False
                self.reproduced = time.time()
                if self.target.fertile and random.uniform(0, 100) < self.endurance:
                    self.target.pregnant = True
                    self.target.fertile = False
                    self.fitness += 1
                    self.target.fitness += 1
                    self.target.make_baby(self)
                self.target = None
        elif self.target is None:
            self.reproducing = False

    def make_baby(self, mate):
        self.time_pregnant = time.time()
        speed = self.speed + mate.speed
        strength = self.strength + mate.strength
        perception = self.perception + mate.perception
        focus = self.focus + mate.focus
        endurance = self.endurance + mate.endurance
        total = speed + strength + perception + focus + endurance

        child = Organism()
        child.color = (((self.color[0] + mate.color[0]) / 510) * 255, ((self.color[1] + mate.color[1]) / 510) * 255,
                       ((self.color[2] + mate.color[2]) / 510) * 255)
        child.sex = random.choice(['M', 'F'])
        child.speed = (speed / total) * 100
        child.strength = (strength / total) * 100
        child.focus = (focus / total) * 100
        child.perception = (perception / total) * 100
        child.endurance = (endurance / total) * 100
        child.lifetime = (self.strength + self.endurance) * 3
        child.sociability = (self.sociability + mate.sociability) / 2
        child.survivability = (self.survivability + mate.survivability) / 2
        child.parents = [self, mate]
        child.generation = max(self.generation, mate.generation) + 1
        self.baby = child

    def find_herd(self):
        if len(self.organism_perceptions) > 0:
            self.herding = True
            self.reproducing = False
            self.foraging = False
            return random.choice(self.organism_perceptions)

    def herd(self):
        self.herding = True
        self.reproducing = False
        self.foraging = False
        if len(self.organism_perceptions) > 0 and random.uniform(0, 5) < self.sociability:
            self.target = random.choice(self.organism_perceptions)
        elif len(self.organism_perceptions) > 0 and self.fertile and random.uniform(0, 5) < (self.endurance / 50):
            self.find_mate()
        else:
            self.target = None

    def get_dist(self, other):
        return math.sqrt((other.bounds.x - self.bounds.x)**2 +
                         (other.bounds.y - self.bounds.y)**2)

    @staticmethod
    def set_color():
        colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 255, 125), (255, 0, 155)]
        return random.choice(colors)


class Plant:
    def __init__(self, bounds):
        self.bounds = bounds
        self.name = 'Plant'

    def draw(self, display):
        pygame.draw.ellipse(display, (0, 225, 20), self.bounds)
