def apply_drag(object, ratio=0.05):
    object.yv = object.yv * (1 - ratio)
    object.xv = object.xv * (1 - ratio)