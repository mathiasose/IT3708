from math import cos, sin, sqrt


euclidean_distance = lambda a, b: sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def rotate_point(point, r, around):
    translated = point[0] - around[0], point[1] - around[1]
    rotated = (translated[0] * cos(r) - translated[1] * sin(r), translated[0] * sin(r) + translated[1] * cos(r))
    reverse_translated = rotated[0] + around[0], rotated[1] + around[1]
    return reverse_translated


def rotate_polygon(polygon, r=0.0, around=(0, 0)):
    if r == 0:
        return polygon

    return [rotate_point(corner, r, around) for corner in polygon]


def normalize_vector(x, y):
    l = sqrt(x ** 2 + y ** 2)
    if l == 0:
        return 0.0, 0.0

    return float(x) / l, float(y) / l
