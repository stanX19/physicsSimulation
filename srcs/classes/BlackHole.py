import math
import pygame
from srcs.conf import conf
from srcs.classes.Sphere import Sphere


class BlackHole():
    def __init__(self, x=-1, y=-1, xv=0, yv=0, rad=10, mass=10000, color=(255, 255, 255), visible=True, deleting=False, **kwargs):
        self.x = x if x != -1 else conf.Status.CENTER[0]
        self.y = y if y != -1 else conf.Status.CENTER[1]
        self.xv = xv
        self.yv = yv
        self.rad = rad
        self.mass = mass
        self.color = color
        self.visible = visible
        self.deleting = deleting

    def attract(self, other):
        if isinstance(other, Sphere):
            x_dis = self.x - other.x
            y_dis = self.y - other.y
            dis = math.sqrt(x_dis**2 + y_dis**2)
            G = 0.01
            fps = 30
            acceleration = G * self.mass / dis ** 2
            other.xv += (x_dis / dis) * (acceleration / fps)
            other.yv += (y_dis / dis) * (acceleration / fps)

    def draw(self, window=None):
        if window is None:
            window = conf.Status.WINDOW
        pygame.draw.circle(window, self.color, (self.x, self.y), self.rad)