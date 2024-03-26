import pygame.draw
from srcs.classes.Sphere import Sphere
from srcs.classes.Line import Line
from srcs.conf import conf
import math

class Barrier(Line):
    def __init__(self, x1, y1, x2, y2, color=(255, 255, 255), **kwargs):
        super(Barrier, self).__init__(x1, y1, x2, y2)
        self.color = color

    def _collide_if_contact__sphere(self, target: Sphere):
        if min(self.x1, self.x2) > target.x + target.rad:
            return
        if max(self.x1, self.x2) < target.x - target.rad:
            return
        if min(self.y1, self.y2) > target.y + target.rad:
            return
        if max(self.y1, self.y2) < target.y - target.rad:
            return

        closest_x, closest_y = self.closest_point_to(target.x, target.y)
        distance = math.hypot(target.x - closest_x, target.y - closest_y)

        if distance > target.rad:
            return

        # Calculate the normal vector from the barrier to the sphere
        normal_x = target.x - closest_x
        normal_y = target.y - closest_y

        # Normalize the normal vector
        normal_length = math.hypot(normal_x, normal_y)

        if normal_length == 0:
            return

        normal_x /= normal_length
        normal_y /= normal_length

        # cancel impulse towards barrier, normal vec towards target
        impulse_cancel = -min(0, target.impulse_x * normal_x + target.impulse_y * normal_y)
        target.impulse_x += impulse_cancel * normal_x
        target.impulse_y += impulse_cancel * normal_y

        # Calculate the dot product of the sphere's velocity and the normal vector
        dot_product = target.xv * normal_x + target.yv * normal_y

        # If the dot product is negative, the sphere is moving towards the barrier
        if dot_product < 0:
            # Calculate the reflection vector
            reflection_x = 2 * dot_product * normal_x
            reflection_y = 2 * dot_product * normal_y

            # Update the sphere's velocity using the reflection vector
            target.impulse_x -= reflection_x * target.mass
            target.impulse_y -= reflection_y * target.mass

        # Repel the sphere
        distance_needed = target.rad - distance
        target.x += normal_x * distance_needed
        target.y += normal_y * distance_needed


    def collide_if_contact(self, target):
        if isinstance(target, Sphere):
            self._collide_if_contact__sphere(target)
        else:
            raise ValueError(f"Barrier: Undefined behavior with type {type(target)}")

    def draw(self, window=None):
        if window is None:
            window = conf.Status.WINDOW
        pygame.draw.line(window, self.color, (self.x1, self.y1), (self.x2, self.y2))
