from srcs.visuals.draw_arrow import draw_arrow
from srcs.classes.Sphere import Sphere
from srcs.conf import conf

def print_vector(target:Sphere, width = 0.5, scale = 10, head = 5):
    draw_arrow(conf.Status.WINDOW, conf.colors["BLUE"],
               (target.x, target.y),
               (target.x + target.xv, target.y),
               width, scale, head)
    draw_arrow(conf.Status.WINDOW, conf.colors["RED"],
               (target.x, target.y),
               (target.x, target.y + target.yv),
               width, scale, head)
    draw_arrow(conf.Status.WINDOW, conf.colors["LIME"],
               (target.x, target.y),
               (target.x + target.xv, target.y + target.yv),
               width, scale, head)