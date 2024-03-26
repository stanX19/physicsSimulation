from srcs.classes.Sphere import Sphere
import math


def sphere_sphere_repel(ball_A: Sphere, ball_B: Sphere):
    normal_x = ball_A.x - ball_B.x
    normal_y = ball_A.y - ball_B.y
    dis = math.hypot(normal_x, normal_y)
    if dis == 0:
        dis = 0.00000000000001

    displacement_needed = ball_A.rad + ball_B.rad - dis
    normal_x /= dis
    normal_y /= dis

    # # ratio
    # total_rad = ball_A.rad + ball_B.rad
    # A_ratio = ball_A.rad / total_rad
    # B_ratio = ball_B.rad / total_rad
    #
    # # Can try to negate the sign, very fun, will move like lifeform
    # ball_A.x += normal_x * displacement_needed * A_ratio
    # ball_A.y += normal_y * displacement_needed * A_ratio
    # ball_B.x -= normal_x * displacement_needed * B_ratio
    # ball_B.y -= normal_y * displacement_needed * B_ratio

    if ball_A.rad < ball_B.rad:
        ball_A.x += normal_x * displacement_needed
        ball_A.y += normal_y * displacement_needed
    else:
        ball_B.x -= normal_x * displacement_needed
        ball_B.y -= normal_y * displacement_needed
