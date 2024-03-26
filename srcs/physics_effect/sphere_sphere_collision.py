from srcs.classes.Sphere import Sphere
import math
import random


# def sphere_sphere_collision0(ball_A: Sphere, ball_B: Sphere):
#     y_dis = ball_A.y - ball_B.y
#     x_dis = ball_A.x - ball_B.x
#     dis = math.sqrt((x_dis) ** 2 + (y_dis) ** 2)
#     if dis == 0:
#         ball_A.x += random.uniform(-1, 1)
#         ball_A.y += random.uniform(-1, 1)
#         y_dis = ball_A.y - ball_B.y
#         x_dis = ball_A.x - ball_B.x
#         dis = math.sqrt((x_dis) ** 2 + (y_dis) ** 2)
#
#     y_over_dis = y_dis / dis
#     x_over_dis = x_dis / dis
#
#     ball_A_tan = (ball_A.yv * -x_over_dis + ball_A.xv * y_over_dis)
#     ball_A_norm = (ball_A.yv * y_over_dis + ball_A.xv * x_over_dis)
#
#     ball_B_tan = (ball_B.yv * -x_over_dis + ball_B.xv * y_over_dis)
#     ball_B_norm = (ball_B.yv * y_over_dis + ball_B.xv * x_over_dis)
#
#     # formula src: https://www.vobarian.com/collisions/2dcollisions2.pdf
#     ball_A_final_norm = (ball_A_norm * (ball_A.mass - ball_B.mass) + 2 * ball_B.mass * ball_B_norm) \
#                       / (ball_A.mass + ball_B.mass)
#     ball_B_final_norm = (ball_B_norm * (ball_B.mass - ball_A.mass) + 2 * ball_A.mass * ball_A_norm) \
#                      / (ball_B.mass + ball_A.mass)
#
#     ball_A.xv = ball_A_tan * y_over_dis + ball_A_final_norm * x_over_dis
#     ball_A.yv = ball_A_tan * -x_over_dis + ball_A_final_norm * y_over_dis
#
#     ball_B.xv = ball_B_tan * y_over_dis + ball_B_final_norm * x_over_dis
#     ball_B.yv = ball_B_tan * -x_over_dis + ball_B_final_norm * y_over_dis


def dot_product(vector1, vector2):
    if len(vector1) != len(vector2):
        raise ValueError("Vectors must have the same length")

    result = sum(a * b for a, b in zip(vector1, vector2))
    return result


def sphere_sphere_collision1(ball_A: Sphere, ball_B: Sphere):
    normal_vector = [ball_B.x - ball_A.x, ball_B.y - ball_A.y]  # A to B

    dis = math.hypot(*normal_vector)
    if dis == 0:
        normal_vector[0] += random.uniform(-1, 1)
        normal_vector[1] += random.uniform(-1, 1)
        dis = math.hypot(*normal_vector)

    normal_unit_vector = [normal_vector[0] / dis, normal_vector[1] / dis]

    u1 = dot_product([ball_A.xv, ball_A.yv], normal_unit_vector)  # dot product
    u2 = dot_product([ball_B.xv, ball_B.yv], normal_unit_vector)  # dot product

    # cancel out impulse towards each other
    # impulse_cancel = max(0, dot_product([ball_A.impulse_x, ball_A.impulse_y], normal_unit_vector)) - \
    #                  min(0, dot_product([ball_B.impulse_x, ball_B.impulse_y], normal_unit_vector))
    # ball_A.impulse_x -= impulse_cancel * normal_unit_vector[0]
    # ball_A.impulse_y -= impulse_cancel * normal_unit_vector[1]
    # ball_B.impulse_x += impulse_cancel * normal_unit_vector[0]
    # ball_B.impulse_y += impulse_cancel * normal_unit_vector[1]

    if not u1 - u2 > 0:  # not moving towards each other, seperating
        return 0

    m1 = ball_A.mass
    m2 = ball_B.mass
    e = ball_A.elasticity * ball_B.elasticity

    impulse_A = m1 * (u1 * m1 + u2 * m2 - m2 * e * (u1 - u2)) / (m1 + m2) - m1 * u1
    impulse_B = m2 * (u1 * m1 + u2 * m2 - m1 * e * (u2 - u1)) / (m1 + m2) - m2 * u2

    ball_A.impulse_x += impulse_A * normal_unit_vector[0]
    ball_A.impulse_y += impulse_A * normal_unit_vector[1]
    ball_B.impulse_x += impulse_B * normal_unit_vector[0]
    ball_B.impulse_y += impulse_B * normal_unit_vector[1]

    ball_A.updated = True
    ball_B.updated = True

    return 1


def sphere_sphere_collision(ball_A: Sphere, ball_B: Sphere):
    normal_vector = [ball_B.x - ball_A.x, ball_B.y - ball_A.y]  # A to B

    dis = math.hypot(*normal_vector)
    if dis == 0:
        normal_vector[0] += random.uniform(-1, 1)
        normal_vector[1] += random.uniform(-1, 1)
        dis = math.hypot(*normal_vector)

    normal_unit_vector = [normal_vector[0] / dis, normal_vector[1] / dis]

    u1 = dot_product([ball_A.xv, ball_A.yv], normal_unit_vector)  # dot product
    u2 = dot_product([ball_B.xv, ball_B.yv], normal_unit_vector)  # dot product

    if not u1 - u2 > 0:  # not moving towards each other, seperating
        return 0

    m1 = ball_A.mass
    m2 = ball_B.mass
    e = ball_A.elasticity * ball_B.elasticity

    impulse_A = (u1 * m1 + u2 * m2 - m2 * e * (u1 - u2)) / (m1 + m2) - u1
    impulse_B = (u1 * m1 + u2 * m2 - m1 * e * (u2 - u1)) / (m1 + m2) - u2

    ball_A.xv += impulse_A * normal_unit_vector[0]
    ball_A.yv += impulse_A * normal_unit_vector[1]
    ball_B.xv += impulse_B * normal_unit_vector[0]
    ball_B.yv += impulse_B * normal_unit_vector[1]

    ball_A.updated = True
    ball_B.updated = True

    return 1
