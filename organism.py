import pygame
import random
import math
import time


class Organism:
    def __init__(self, x_pos=None, y_pos=None):
        if x_pos is not None and y_pos is not None:
            self.bounds = pygame.Rect(x_pos, y_pos, 15, 15)
            self.center = (x_pos, y_pos)
        else:
            x_pos = random.uniform(20, 780)
            y_pos = random.uniform(20, 780)
            self.bounds = pygame.Rect(x_pos, y_pos, 15, 15)
            self.center = (x_pos, y_pos)
        self.color = (random.uniform(0, 255), random.uniform(0, 255), random.uniform(0, 255))
        self.birth = time.time()
        self.age = 0
        self.name = 'Organism ' + str(self.color)
        self.parents = []
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
        self.children = []
        self.hungry = False
        self.time_pregnant = 0
        self.eating = False
        self.target = None
        self.predator = None
        self.mouth = 0
        self.reproduced = time.time()
        self.ate = time.time()
        self.hunger = None
        # perceptions
        self.plant_perceptions = []
        self.organism_perceptions = []
        self.predator_perceptions = []

    def __repr__(self):
        return '\nSpeed: ' + str(self.speed) + '\nStrength: ' + str(self.strength) + \
               '\nFocus: ' + str(self.focus) + '\nPerception: ' + str(self.perception) + \
               '\nEndurance: ' + str(self.endurance) + '\nSurvivability: ' + str(self.survivability) + \
               '\nSociability: ' + str(self.sociability) + '\nSex: ' + str(self.sex) + \
               '\nPlants Eaten: ' + str(self.food_eaten) + '\nPregnant: ' + str(self.pregnant) + \
               '\nHerding: ' + str(self.herding) + '\nReproducing: ' + str(self.reproducing) + \
               '\nForaging: ' + str(self.foraging) + '\nAge: ' + str(self.age) + \
               '\nLifetime: ' + str(self.lifetime) + '\nPerceptions: ' + str(self.plant_perceptions) + \
               '\nTarget: ' + str(self.target.__class__) + '\nGeneration: ' + str(self.generation) + '\n'

    # draw the organism based on their bounds
    def draw(self, display):
        pygame.draw.rect(display, self.color, self.bounds)
        pygame.draw.circle(display, (255, 255, 255), (int(self.bounds.x + self.bounds.width / 4), self.bounds.y + 5), 3)
        pygame.draw.circle(display, (255, 255, 255), (int(self.bounds.x + self.bounds.width - 4), self.bounds.y + 5), 3)
        pygame.draw.circle(display, (0, 0, 0), (int(self.bounds.x + self.bounds.width / 4), self.bounds.y + 5), 1)
        pygame.draw.circle(display, (0, 0, 0), (int(self.bounds.x + self.bounds.width - 4), self.bounds.y + 5), 1)

        # draw the organism's mouth
        if not self.eating:
            pygame.draw.line(display, (255, 255, 255), (self.bounds.x + 3, self.bounds.y + self.bounds.height - 4),
                             (self.bounds.x + self.bounds.width - 3, self.bounds.y + self.bounds.height - 4), 1)
        # if the organism is eating, draw the mouth but make it eat :^)
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

    # decide where the organism moves, be it towards a target or randomly
    def move(self, width, height):
        if random.uniform(0, 50) <= 10:
            # if there are predators nearby
            if len(self.predator_perceptions) > 1 and random.uniform(0, 3) < self.survivability:
                self.flee()
                delta_x, delta_y = self.run_from_predator()
            # if there is no target, move randomly
            elif self.target is None:
                delta_x, delta_y = self.move_randomly()
            # if the organism is herding, move randomly with the herd
            elif self.herding:
                if self.get_dist(self.target) <= self.perception * 8:
                    delta_x, delta_y = self.move_randomly()
                else:
                    delta_x, delta_y = self.move_towards_target()
            # if the organism is not herding, move directly towards the target
            else:
                delta_x, delta_y = self.move_towards_target()

            if self.bounds.width < self.center[0] + delta_x < width \
                    and self.bounds.height < self.center[1] + delta_y < height:
                self.bounds = self.bounds.move((delta_x, delta_y))
                self.center = (self.center[0] + delta_x, self.center[1] + delta_y)

    # once a target has been chosen, move towards it with a distance correlated to the organisms speed
    def move_towards_target(self):
        if self.center[0] < self.target.center[0]:
            delta_x = random.uniform(self.speed / 10, self.speed / 2)
            if self.center[1] < self.target.center[1]:
                delta_y = random.uniform(self.speed / 10, self.speed / 2)
            elif self.center[1] > self.target.center[1]:
                delta_y = random.uniform(-self.speed / 2, -self.speed / 10)
            else:
                delta_y = 0
        elif self.center[0] > self.target.center[0]:
            delta_x = random.uniform(-self.speed / 2, -self.speed / 10)
            if self.center[1] < self.target.center[1]:
                delta_y = random.uniform(self.speed / 10, self.speed / 2)
            elif self.center[1] > self.target.center[1]:
                delta_y = random.uniform(-self.speed / 2, -self.speed / 10)
            else:
                delta_y = 0
        elif self.center[0] == self.target.center[0] and self.center[1] == self.target.center[1]:
            delta_x, delta_y = self.move_randomly()
        else:
            delta_x = 0
            if self.center[1] < self.target.center[1]:
                delta_y = random.uniform(self.speed / 10, self.speed / 2)
            elif self.center[1] > self.target.center[1]:
                delta_y = random.uniform(-self.speed / 2, -self.speed / 10)
            else:
                delta_y = 0
        return delta_x, delta_y

    # once a target has been chosen, move towards it with a distance correlated to the organisms speed
    def run_from_predator(self):
        if self.center[0] < self.predator.center[0]:
            delta_x = random.uniform(self.speed / 10, self.speed / 2)
            if self.center[1] < self.predator.center[1]:
                delta_y = random.uniform(self.speed / 10, self.speed / 2)
            elif self.center[1] > self.predator.center[1]:
                delta_y = random.uniform(-self.speed / 2, -self.speed / 10)
            else:
                delta_y = 0
        elif self.center[0] > self.predator.center[0]:
            delta_x = random.uniform(-self.speed / 2, -self.speed / 10)
            if self.center[1] < self.predator.center[1]:
                delta_y = random.uniform(self.speed / 10, self.speed / 2)
            elif self.center[1] > self.predator.center[1]:
                delta_y = random.uniform(-self.speed / 2, -self.speed / 10)
            else:
                delta_y = 0
        elif self.center[0] == self.predator.center[0] and self.center[1] == self.predator.center[1]:
            delta_x, delta_y = self.move_randomly()
        else:
            delta_x = 0
            if self.center[1] < self.predator.center[1]:
                delta_y = random.uniform(self.speed / 10, self.speed / 2)
            elif self.center[1] > self.predator.center[1]:
                delta_y = random.uniform(-self.speed / 2, -self.speed / 10)
            else:
                delta_y = 0
        return -delta_x, -delta_y

    # move in a random direction with a distance correlated to the organisms speed
    def move_randomly(self):
        delta_x = random.uniform((-self.speed / 2), self.speed / 2)
        delta_y = random.uniform((-self.speed / 2), self.speed / 2)
        return delta_x, delta_y

    # with every game tick, make the organism get older
    def get_older(self, population):
        self.age = time.time() - self.birth

        # control "puberty" and other age related triggers
        if self.age > self.lifetime:
            self.die(population)
        elif not self.fertile and self.age >= self.lifetime / 3 and self.food_eaten > 0:
            self.fertile = True
        elif not self.fertile and time.time() - self.reproduced > self.lifetime / (((100 - self.endurance) / 100) * 10):
            self.fertile = True

        # causes the organism to become hungry after a certain time threshold
        if not self.hungry and time.time() - self.ate >= (self.age / 5 + self.endurance / 2):
            self.hungry = True
            self.hunger = time.time()
        # if the organism goes too long without eating, start to die
        if self.hungry and time.time() - self.hunger >= (self.age / 5 + self.endurance / 2):
            self.die(population)

        # start cooking up a baby
        if self.pregnant:
            if time.time() - self.time_pregnant > self.lifetime / 10:
                self.baby.bounds.x, self.baby.bounds.y = self.bounds.x, self.bounds.y
                population.append(self.baby)
                self.children.append(self.baby)
                print('Birth, population: ', len(population))
                self.fertile = False
                self.pregnant = False
                self.baby = None
                self.time_pregnant = 0

    # slowly kill the organism
    def die(self, population):
        if self.bounds.width > 0 and random.uniform(0, 100) < 10:
            self.speed = self.speed / 2
            self.focus = self.focus / 2
            self.bounds.width -= 1
            self.bounds.height -= 1
        elif self.bounds.width == 0:
            population.remove(self)
            print('Death, population: ', len(population))

    # generate random stats for an organism
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
        # normalize the stats over a scale of [0, 100]
        self.speed = (speed / total) * 100
        self.strength = (strength / total) * 100
        self.focus = (focus / total) * 100
        self.perception = (perception / total) * 100
        self.endurance = (endurance / total) * 100
        self.lifetime = (self.strength + self.endurance) * 4

    # perceive the world around the organism
    def perceive(self, population):
        self.plant_perceptions = []
        self.organism_perceptions = []
        for organism in population:
            if self.get_dist(organism) <= self.perception * 7:
                if organism.__class__ == Plant and organism not in self.plant_perceptions:
                    self.plant_perceptions.append(organism)
                elif organism.__class__ == Organism and organism not in self.organism_perceptions:
                    self.organism_perceptions.append(organism)
                elif organism.__class__ == Predator and organism not in self.predator_perceptions:
                    self.predator_perceptions.append(organism)

    # make an action decision based on the organism's perceptions
    def decide(self):
        if self.target is None or time.time() - self.focus_time > self.focus:
            # self.reset_status()
            # if fertile and endurance is high enough
            if self.fertile and not self.pregnant and random.uniform(0, 50) < self.endurance:
                self.find_mate()
            # if hungry and there is food around OR if survivability is high enough
            elif (self.hungry and len(self.plant_perceptions) > 0) or \
                 (len(self.plant_perceptions) > 0 and random.uniform(0, 5) < self.survivability):
                self.find_food()
            # if there are friends around the sociability is high enough
            elif len(self.organism_perceptions) > 0 and random.uniform(0, 5) < self.sociability:
                self.find_herd()
            else:
                self.target = None

    # act based on the decision made
    def act(self):
        if self.herding:
            self.herd()
        elif self.reproducing and self.fertile:
            self.mate()

    # choose a food target
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

    # find a mate target
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
            if self.target in self.children or self.target in self.parents or\
                    self.target.__class__ != self.__class__:
                self.target = None
                self.reproducing = False

                self.target = None
                self.reproducing = False
        else:
            self.target = None
            self.reproducing = False

    # run from predators
    def flee(self):
        self.predator = random.choice(self.predator_perceptions)
        if self.predator.bounds.width < self.bounds.width:
            self.predator = None

    # attempt to mate with the mate target
    def mate(self):
        if self.target is not None and self.target and self.bounds.colliderect(self.target.bounds):
            self.fertile = False
            if self.sex == 'F' and not self.pregnant and self.target.fertile:
                self.reproducing = False
                self.reproduced = time.time()
                if self.target.fertile and random.uniform(0, 50) < self.endurance:
                    self.pregnant = True
                    self.fitness += 1
                    self.target.fitness += 1
                    self.make_baby(self.target)
                self.target = None
            elif self.sex == 'M' and self.target.fertile:
                self.reproducing = False
                self.reproduced = time.time()
                if self.target.fertile and random.uniform(0, 50) < self.endurance:
                    self.target.pregnant = True
                    self.target.fertile = False
                    self.fitness += 1
                    self.target.fitness += 1
                    self.target.make_baby(self)
                self.target = None
        elif self.target is None:
            self.reproducing = False

    # if a mate was successful, begin creating a baby with stats blended with mom and dad
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
        mate.children.append(self.baby)

    # find other organisms to herd with
    def find_herd(self):
        if len(self.organism_perceptions) > 0:
            self.herding = True
            self.reproducing = False
            self.foraging = False
            target = random.choice(self.organism_perceptions)
            if target.__class__ == self.__class__:
                self.target = target
            else:
                self.target = None

    # herd with the herd target
    def herd(self):
        self.herding = True
        self.reproducing = False
        self.foraging = False
        if self.hungry:
            self.find_food()
        elif len(self.organism_perceptions) > 0 and random.uniform(0, 5) < self.sociability:
            self.target = random.choice(self.organism_perceptions)
        elif len(self.organism_perceptions) > 0 and self.fertile and random.uniform(0, 5) < (self.endurance / 50):
            self.find_mate()
        else:
            self.target = None

    # get the distance between the organism and the target, other
    def get_dist(self, other):
        return math.sqrt((other.bounds.x - self.bounds.x)**2 +
                         (other.bounds.y - self.bounds.y)**2)

    # set the organisms color
    @staticmethod
    def set_color():
        colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 255, 125), (255, 0, 155)]
        return random.choice(colors)


class Plant:
    def __init__(self, bounds):
        self.bounds = bounds
        self.center = (self.bounds.x, self.bounds.y)
        self.name = 'Plant'

    def draw(self, display):
        pygame.draw.ellipse(display, (0, 225, 20), self.bounds)


class Predator(Organism):
    def __init__(self, x_pos=None, y_pos=None):
        Organism.__init__(self)
        if x_pos is not None and y_pos is not None:
            self.bounds = pygame.Rect(x_pos, y_pos, 25, 25)
            self.center = (x_pos, y_pos)
        else:
            x_pos = int(random.uniform(20, 780))
            y_pos = int(random.uniform(20, 780))
            self.bounds = pygame.Rect(x_pos, y_pos, 25, 25)
            self.center = (x_pos, y_pos)
        self.color = (random.uniform(0, 255), random.uniform(0, 255), random.uniform(0, 255))
        self.birth = time.time()
        self.age = 0
        self.name = 'Predator ' + str(self.color)
        self.parents = []
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
        self.children = []
        self.hungry = False
        self.time_pregnant = 0
        self.eating = False
        self.target = None
        self.prey = None
        self.mouth = 0
        self.reproduced = time.time()
        self.ate = time.time()
        self.hunger = None
        # perceptions
        self.plant_perceptions = []
        self.organism_perceptions = []
        self.prey_perceptions = []

    def draw(self, display):
        pygame.draw.circle(display, self.color, self.center, int(self.bounds.width / 2), 0)

        pygame.draw.circle(display, (255, 255, 255), (self.center[0] - 7, self.center[1] - 5), 3)
        pygame.draw.circle(display, (255, 255, 255), (self.center[0] + 7, self.center[1] - 5), 3)
        pygame.draw.circle(display, (0, 0, 0), (self.center[0] - 7, self.center[1] - 5), 1)
        pygame.draw.circle(display, (0, 0, 0), (self.center[0] + 7, self.center[1] - 5), 1)

        # if the organism is eating, draw the mouth but make it eat :^)
        if self.eating:
            pygame.draw.circle(display, (255, 255, 255), (self.center[0], self.center[1] + 5), self.mouth)
            if self.mouth < int(self.bounds.width / 4):
                if random.uniform(0, 1) < 0.2:
                    self.mouth += 1
            else:
                self.eating = False
                self.mouth = 1
        else:
            pygame.draw.line(display, (255, 255, 255), (self.center[0] - 5, self.center[1] + 5),
                             (self.center[0] + 5, self.center[1] + 5), 1)

    # decide where the organism moves, be it towards a target or randomly
    def move(self, width, height):
        if random.uniform(0, 50) <= 10:
            # if there is no target, move randomly
            if self.target is None:
                delta_x, delta_y = self.move_randomly()
            # if the organism is herding, move randomly with the herd
            elif self.herding:
                if self.get_dist(self.target) <= self.perception * 8:
                    delta_x, delta_y = self.move_randomly()
                else:
                    delta_x, delta_y = self.move_towards_target()
            # if the organism is not herding, move directly towards the target
            else:
                delta_x, delta_y = self.move_towards_target()

            if self.bounds.width < self.center[0] + delta_x < width \
                    and self.bounds.height < self.center[1] + delta_y < height:
                self.center = (int(self.center[0] + delta_x), int(self.center[1] + delta_y))

    # perceive the world around the organism
    def perceive(self, population):
        self.plant_perceptions = []
        self.organism_perceptions = []
        self.prey_perceptions = []
        for organism in population:
            if self.get_dist(organism) <= self.perception * 7:
                if organism.__class__ == Plant and organism not in self.plant_perceptions:
                    self.plant_perceptions.append(organism)
                elif organism.__class__ == Predator and organism not in self.organism_perceptions:
                    self.organism_perceptions.append(organism)
                elif organism.__class__ == Organism and organism not in self.prey_perceptions:
                    self.prey_perceptions.append(organism)

    # choose a food target
    def find_food(self):
        if len(self.prey_perceptions) > 0:
            self.foraging = True
            self.reproducing = False
            self.herding = False
            self.focus_time = time.time()
            self.target = random.choice(self.prey_perceptions)
            self.prey = self.target
        else:
            self.foraging = False
            self.reproducing = False
            self.herding = False
            self.target = None

    def can_eat(self, target):
        if not target.herding and self.get_dist(target) < self.bounds.width / 4 and \
                self.bounds.width > target.bounds.width:
            return True
        return False

    def get_dist(self, other):
        return math.sqrt((other.center[0] - self.center[0])**2 +
                         (other.center[1] - self.center[1])**2)

    # with every game tick, make the organism get older
    def get_older(self, population):
        self.age = time.time() - self.birth

        # control "puberty" and other age related triggers
        if self.age > self.lifetime:
            self.die(population)
        elif not self.fertile and self.age >= self.lifetime / 3 and self.food_eaten > 0:
            self.fertile = True
        elif not self.fertile and time.time() - self.reproduced > self.lifetime / (((100 - self.endurance) / 100) * 10):
            self.fertile = True

        # causes the organism to become hungry after a certain time threshold
        if not self.hungry and time.time() - self.ate >= (self.age / 4 + self.endurance):
            self.hungry = True
            self.hunger = time.time()
        # if the organism goes too long without eating, start to die
        if self.hungry and time.time() - self.hunger >= (self.age / 4 + self.endurance):
            self.die(population)

        # start cooking up a baby
        if self.pregnant:
            if time.time() - self.time_pregnant > self.lifetime / 10:
                self.baby.bounds.x, self.baby.bounds.y = self.bounds.x, self.bounds.y
                population.append(self.baby)
                self.children.append(self.baby)
                print('Birth, population: ', len(population))
                self.fertile = False
                self.pregnant = False
                self.baby = None
                self.time_pregnant = 0
