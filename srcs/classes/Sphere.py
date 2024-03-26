import math
import pygame
from srcs.conf import conf


class Sphere:
    def __init__(self, x=0, y=0, xv=0, yv=0, mass=0, color=(255, 255, 255), elasticity=1, **kwargs):
        self.x = x
        self.y = y
        self.xv = xv
        self.yv = yv
        self.impulse_x = 0
        self.impulse_y = 0
        self.mass = mass
        self.color = color
        self.elasticity = elasticity

        self.rad = math.sqrt(mass / 3.142)
        for key, val in kwargs.items():
            setattr(self, key, val)

        self.updated = False

    @property
    def momentum(self):
        return math.hypot(self.xv, self.yv) * self.mass

    @property
    def resultant_vector(self):
        return math.hypot(self.xv, self.yv)

    def update(self):
        # self.color = (min(255, int(math.hypot(self.impulse_x, self.impulse_y))), 255, 0)
        if self.x + self.rad > conf.Status.SCREEN_SIZE[0] and self.xv > 0:
            self.impulse_x = -self.xv * self.mass * 2
        elif self.x - self.rad < 0 and self.xv < 0:
            self.impulse_x = -self.xv * self.mass * 2
        self.xv += self.impulse_x / self.mass / 2
        self.x += self.xv
        self.xv += self.impulse_x / self.mass / 2
        self.impulse_x = 0

        if self.y + self.rad > conf.Status.SCREEN_SIZE[1] and self.yv > 0:
            self.impulse_y = -self.yv * self.mass * 2
        elif self.y - self.rad < 0 and self.yv < 0:
            self.impulse_y = -self.yv * self.mass * 2
        self.yv += self.impulse_y / self.mass / 2
        self.y += self.yv
        self.yv += self.impulse_y / self.mass / 2
        self.impulse_y = 0

        self.updated = True

    def draw(self, window=None):
        if window is None:
            window = conf.Status.WINDOW
        pygame.draw.circle(window, self.color, (self.x, self.y), self.rad)
