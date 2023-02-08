import pygame
import time
import math
import ast
import os
import sys
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from srcs.classes.Sphere import Sphere
from srcs.physics_effect.sphere_sphere_collision import sphere_sphere_collision
from srcs.physics_effect.sphere_sphere_repel import sphere_sphere_repel
from srcs.physics_effect.apply_drag import apply_drag
from srcs.helper.random_balls import random_balls
from srcs.conf import conf
from srcs.visuals.print_vector import print_vector
from srcs.visuals.print_trail import print_trail


def init_pygame():
    pygame.init()
    conf.Status.WINDOW = pygame.display.set_mode(conf.Status.SCREEN_SIZE)
    pygame.display.set_caption("balls bouncing")


def init_data():
    conf.init_configs()
    conf.Status.OBJS = []

    for key, kwargs in conf.Status.object_kwargs.items():
        for _key, val in kwargs.items():
            try:
                kwargs[_key] = ast.literal_eval(val)
            except ValueError:
                if _key == 'color':
                    try:
                        kwargs[_key] = conf.colors[val.upper()]
                    except Exception:
                        raise ValueError(f"Invalid color: {val}")
        if 'sphere' in key:
            conf.Status.OBJS.append(Sphere(**kwargs))
        elif 'random' in key:
            conf.Status.OBJS += random_balls(**kwargs)


def main():
    # up down left right
    pressed = []
    scale = 100
    directions = {82: (0, -scale), 81: (0, scale), 80: (-scale, 0), 79: (scale, 0)}

    # init
    init_data()
    init_pygame()
    clock = pygame.time.Clock()

    while conf.Status.RUNNING:
        clock.tick(60)

        if conf.Status.OBJS.__len__() <= 1:
            time.sleep(1)
            init_data()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                conf.Status.RUNNING = False
            elif event.type == pygame.KEYDOWN:
                pressed.append(event.scancode)
            elif event.type == pygame.KEYUP:
                pressed.remove(event.scancode)

        for key in pressed:
            if key == 21:
                init_data()
            if key in directions:
                for ball in conf.Status.OBJS:
                    ball.yv += directions[key][1] / ball.mass
                    ball.xv += directions[key][0] / ball.mass
            if key == 44:  # space key
                for ball in conf.Status.OBJS:
                    apply_drag(ball, 0.05)

        conf.Status.WINDOW.fill(conf.colors["BACKGROUND"])
        conf.Status.OBJS.sort(key=lambda x: x.x - x.rad)

        for idx, ball in enumerate(conf.Status.OBJS):
            for other in conf.Status.OBJS[idx + 1:]:
                rad = ball.rad + other.rad
                if other.x - ball.x < rad:
                    if math.sqrt((ball.x - other.x) ** 2 + (ball.y - other.y) ** 2) < rad:
                        if conf.Effects.COLLISION:
                            sphere_sphere_collision(ball, other)
                        if conf.Effects.MATTER_REPEL:
                            sphere_sphere_repel(ball, other)
                else:
                    break
            if conf.Effects.GRAVITY:
                ball.yv += conf.Effects.GRAVITY
            if conf.Effects.AIR_RESISTANCE:
                apply_drag(ball, conf.Effects.AIR_RESISTANCE)

        for ball in conf.Status.OBJS:
            ball.update_position()
            ball.draw()
            if conf.Effects.VECTOR:
                print_vector(ball, scale=ball.mass*conf.Effects.VECTOR/100)
            if conf.Effects.TRAIL:
                print_trail(ball)

        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()
