from srcs.classes.Sphere import Sphere
import math


def sphere_sphere_repel(ball_A: Sphere, ball_B: Sphere):
    x_dis = ball_A.x - ball_B.x
    y_dis = ball_A.y - ball_B.y
    dis = math.sqrt(x_dis**2 + y_dis**2)

    displacement_needed = ball_A.rad + ball_B.rad - dis
    dis_ratio = displacement_needed / (ball_A.rad + ball_B.rad)
    if ball_A.rad < ball_B.rad:
        ball_A.x += x_dis * dis_ratio
        ball_A.y += y_dis * dis_ratio
    else:
        ball_B.x -= x_dis * dis_ratio / 2
        ball_B.y -= y_dis * dis_ratio / 2
