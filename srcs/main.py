import pygame
import time
import math
import ast
import os
import sys
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from srcs.classes.Sphere import Sphere
from srcs.classes.BlackHole import BlackHole
from srcs.classes.Barrier import Barrier
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
    conf.Status.BLACKHOLE = []
    conf.Status.BARRIERS = []

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
        elif 'blackhole' in key:
            conf.Status.BLACKHOLE.append(BlackHole(**kwargs))
        elif 'barrier' in key:
            conf.Status.BARRIERS.append(Barrier(**kwargs))


def main():
    # up down left right
    pressed = []
    scale = 100
    directions = {82: (0, -scale), 81: (0, scale), 80: (-scale, 0), 79: (scale, 0)}
    # mouse
    mouse = []

    # init
    init_data()
    init_pygame()
    clock = pygame.time.Clock()

    while conf.Status.RUNNING:
        clock.tick(60)

        # if conf.Status.OBJS.__len__() <= 1:
        #     time.sleep(1)
        #     init_data()

        # Real time interaction
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                conf.Status.RUNNING = False
            elif event.type == pygame.KEYDOWN:
                pressed.append(event.scancode)
            elif event.type == pygame.KEYUP:
                pressed.remove(event.scancode)
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse = []
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = event.pos
            elif event.type == pygame.MOUSEMOTION and mouse:
                mouse = event.pos

        for key in pressed:
            if key == 21:  # R
                init_data()
            if key in directions:
                for ball in conf.Status.OBJS:
                    ball.impulse_y += directions[key][1]
                    ball.impulse_x += directions[key][0]
            if key == 44:  # space key
                for ball in conf.Status.OBJS:
                    apply_drag(ball, 0.05)
        if mouse:
            for ball in conf.Status.OBJS:
                rad = 100
                x_dis = mouse[0] - ball.x
                y_dis = mouse[1] - ball.y
                dis = math.sqrt(x_dis**2 + y_dis**2)
                if abs(dis) < rad:
                    ball.xv = (x_dis * abs(x_dis)/10000) * ball.mass
                    ball.yv = (y_dis * abs(y_dis)/10000) * ball.mass

        # Collision detection
        conf.Status.OBJS.sort(key=lambda b: b.x - b.rad)

        # Blackhole
        to_pop = []
        for black_hole in conf.Status.BLACKHOLE:
            if not black_hole.deleting:
                continue
            for idx, ball in enumerate(conf.Status.OBJS):
                if black_hole.x - 10 <= ball.x <= black_hole.x + 10:
                    if math.hypot(ball.x - black_hole.x, ball.y - black_hole.y) < ball.rad + 10:
                        to_pop.append(idx)

        conf.Status.OBJS = [ball for idx, ball in enumerate(conf.Status.OBJS) if idx not in to_pop]
            
        # Sphere velocity update
        while any(obj.updated for obj in conf.Status.OBJS):
            for idx, ball in enumerate(conf.Status.OBJS):
                for other in conf.Status.OBJS[idx + 1:]:
                    rad = ball.rad + other.rad
                    if other.x - ball.x > rad:
                        break
                    if not ball.updated and not other.updated:
                        continue
                    if math.hypot(ball.x - other.x, ball.y - other.y) > rad:
                        continue
                    if conf.Effects.COLLISION:
                        sphere_sphere_collision(ball, other)
                    if conf.Effects.MATTER_REPEL:
                        sphere_sphere_repel(ball, other)
                ball.updated = False

        for idx, ball in enumerate(conf.Status.OBJS):
            for black_hole in conf.Status.BLACKHOLE:
                black_hole.attract(ball)
            if conf.Effects.GRAVITY:
                ball.impulse_y += conf.Effects.GRAVITY * ball.mass
            if conf.Effects.AIR_RESISTANCE:
                apply_drag(ball, conf.Effects.AIR_RESISTANCE)

        for ball in conf.Status.OBJS:
            for barrier in conf.Status.BARRIERS:
                barrier.collide_if_contact(ball)

        # Position update & rendering
        # Background
        conf.Status.WINDOW.fill(conf.colors["BACKGROUND"])

        for ball in conf.Status.OBJS:
            ball.update()
            ball.draw()
            if conf.Effects.VECTOR:
                print_vector(ball, scale=ball.mass*conf.Effects.VECTOR/100)
            if conf.Effects.TRAIL:
                print_trail(ball)

        for black_hole in conf.Status.BLACKHOLE:
            if black_hole.visible:
                black_hole.draw()

        for barrier in conf.Status.BARRIERS:
            barrier.draw()

        print(sum(ball.mass * (conf.Effects.GRAVITY * ball.y + (ball.resultant_vector ** 2) / 2) for ball in conf.Status.OBJS))
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()
