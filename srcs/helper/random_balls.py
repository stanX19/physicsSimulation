import random
from srcs.classes.Sphere import Sphere
from srcs.conf import conf


def random_balls(
            count=10,
            mass_range=(100, 100),
            x_range=(0, conf.Status.SCREEN_SIZE[0]),
            y_range=(0, conf.Status.SCREEN_SIZE[1]),
            xv_range=(-1, 1),
            yv_range=(-1, 1),
            color_range=((100, 255), (100, 255), (100, 255)),
            elasticity_range=(1, 1),
            **kwargs
        ):

    balls = []
    for i in range(count):
        mass = random.uniform(*mass_range)
        x = random.uniform(*x_range)
        y = random.uniform(*y_range)
        xv = random.uniform(*xv_range)
        yv = random.uniform(*yv_range)
        color = tuple(random.randint(*c) for c in color_range) if "color" not in kwargs else kwargs["color"]
        elasticity = random.uniform(*elasticity_range)
        balls.append(Sphere(x, y, xv, yv, mass, color, elasticity))
    return balls
