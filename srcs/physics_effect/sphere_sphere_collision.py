from srcs.classes.Sphere import Sphere
import math


def sphere_sphere_collision(ball_A: Sphere, ball_B: Sphere):
    y_dis = ball_A.y - ball_B.y
    x_dis = ball_A.x - ball_B.x
    dis = math.sqrt((x_dis) ** 2 + (y_dis) ** 2)
    if dis == 0:
        ball_A.x -= 1
        ball_A.y -= 1
        y_dis = ball_A.y - ball_B.y
        x_dis = ball_A.x - ball_B.x
        dis = math.sqrt((x_dis) ** 2 + (y_dis) ** 2)

    y_over_dis = y_dis / dis
    x_over_dis = x_dis / dis

    ball_A_tan = (ball_A.yv * -x_over_dis + ball_A.xv * y_over_dis)
    ball_A_norm = (ball_A.yv * y_over_dis + ball_A.xv * x_over_dis)

    ball_B_tan = (ball_B.yv * -x_over_dis + ball_B.xv * y_over_dis)
    ball_B_norm = (ball_B.yv * y_over_dis + ball_B.xv * x_over_dis)

    # formula src: https://www.vobarian.com/collisions/2dcollisions2.pdf
    ball_A_final_norm = (ball_A_norm * (ball_A.mass - ball_B.mass) + 2 * ball_B.mass * ball_B_norm) \
                      / (ball_A.mass + ball_B.mass)
    obj_final_norm = (ball_B_norm * (ball_B.mass - ball_A.mass) + 2 * ball_A.mass * ball_A_norm) \
                     / (ball_B.mass + ball_A.mass)

    ball_A.xv = ball_A_tan * y_over_dis + ball_A_final_norm * x_over_dis
    ball_A.yv = ball_A_tan * -x_over_dis + ball_A_final_norm * y_over_dis

    ball_B.xv = ball_B_tan * y_over_dis + obj_final_norm * x_over_dis
    ball_B.yv = ball_B_tan * -x_over_dis + obj_final_norm * y_over_dis
