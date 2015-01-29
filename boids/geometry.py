from math import cos, sin


def rotate_point(point, r, around):
    translated = point[0] - around[0], point[1] - around[1]
    rotated = (translated[0] * cos(r) - translated[1] * sin(r), translated[0] * sin(r) + translated[1] * cos(r))
    reverse_translated = rotated[0] + around[0], rotated[1] + around[1]
    return reverse_translated


def rotate_polygon(polygon, r=0.0, around=(0, 0)):
    if r == 0:
        return polygon

    return [rotate_point(corner, r, around) for corner in polygon]