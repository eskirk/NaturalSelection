import pygame


class Plant:
    def __init__(self, bounds):
        self.bounds = bounds
        self.center = (self.bounds.x, self.bounds.y)
        self.name = 'Plant'

    def draw(self, display):
        pygame.draw.ellipse(display, (0, 225, 20), self.bounds)
