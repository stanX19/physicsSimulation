import math
import pygame
from srcs.conf import conf

class Sphere():
    def __init__(self, x=0, y=0, xv=0, yv=0, mass=0, color=(255, 255, 255), elasticity=1, **kwargs):
        self.x = x
        self.y = y
        self.xv = xv
        self.yv = yv
        self.mass = mass
        self.color = color
        self.elasticity = elasticity

        for key, val in kwargs.items():
            setattr(self, key, val)
        self.rad = math.sqrt(mass / 3.142)

    @property
    def momentum(self):
        return math.sqrt((self.xv) ** 2 + (self.yv) ** 2) * self.mass
    @property
    def resultant_vector(self):
        return math.sqrt((self.xv) ** 2 + (self.yv) ** 2)

    def update_position(self):
        self.x += self.xv
        if self.x + self.rad > conf.Status.SCREEN_SIZE[0]:
            self.xv = -self.xv
            self.x = 2 * conf.Status.SCREEN_SIZE[0] - self.x - 2 * self.rad
        elif self.x - self.rad < 0:
            self.xv = -self.xv
            self.x = -self.x + 2 * self.rad
        self.y += self.yv
        if self.y + self.rad > conf.Status.SCREEN_SIZE[1]:
            self.yv = -self.yv
            self.y = 2 * conf.Status.SCREEN_SIZE[1] - self.y - 2 * self.rad
        elif self.y - self.rad < 0:
            self.yv = -self.yv
            self.y = -self.y + 2 * self.rad

    def draw(self, window=None):
        if window is None:
            window = conf.Status.WINDOW
        pygame.draw.circle(window, self.color, (self.x, self.y), self.rad)