from srcs.visuals.draw_arrow import draw_arrow
from srcs.classes.Sphere import Sphere
from srcs.conf import conf

def print_trail(target:Sphere):
    draw_arrow(conf.Status.WINDOW,
               target.color,
               (target.x, target.y),
               (target.x + target.xv, target.y + target.yv),
               target.rad / 2,
               0,
               -7.3
    )