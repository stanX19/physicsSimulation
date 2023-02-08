import pygame
import math

def draw_arrow(window, color, p1, p2, width = 5, scale = 1, head = 5):
    v1 = [p2[0] - p1[0], p2[1] - p1[1]]
    hypo = math.sqrt(v1[0] ** 2 + v1[1] ** 2)
    if hypo == 0:
        return
    v2 = [v1[1], -v1[0]]
    uv2 = [v2[0] / hypo, v2[1] / hypo]
    uv1 = [v1[0] / hypo, v1[1] / hypo]
    body = hypo * scale - head
    if body < 0:
        return
    vertices = [
        (p1[0] + width * uv2[0], p1[1] + width * uv2[1]),
        (p1[0] + body * uv1[0] + width * uv2[0], p1[1] + body * uv1[1] + width * uv2[1]),
        (p1[0] + body * uv1[0] + 2 * width * uv2[0], p1[1] + body * uv1[1] + 2 * width * uv2[1]),
        (p1[0] + scale * v1[0], p1[1] + scale * v1[1]),
        (p1[0] + body * uv1[0] - 2 * width * uv2[0], p1[1] + body * uv1[1] - 2 * width * uv2[1]),
        (p1[0] + body * uv1[0] - width * uv2[0], p1[1] + body * uv1[1] - width * uv2[1]),
        (p1[0] - width * uv2[0], p1[1] - width * uv2[1]),
    ]
    pygame.draw.polygon(window, color, vertices)