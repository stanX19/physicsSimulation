def apply_drag(ball, ratio=0.05):
    ball.yv = ball.yv * (1 - ratio)
    ball.xv = ball.xv * (1 - ratio)