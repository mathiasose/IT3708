from math import pi
from random import randint
import sys
import pygame
from time import sleep

from geometry import rotate_polygon


WINDOW_DIMENSIONS = (1800, 1000)
BACKGROUND = (255, 255, 255)
FOREGROUND = (0, 0, 0)

random_color = lambda: (randint(0, 255), randint(0, 255), randint(0, 255))


class PointyShape(object):
    def __init__(self, x, y, scale=1.0, rotation=0.0, color=FOREGROUND):
        self.x = x
        self.y = y
        self.scale = scale
        self.rotation = rotation
        self.color = color

    @property
    def center(self):
        return self.x, self.y

    def rotate(self, dr):
        self.rotation += dr
        self.rotation %= 2 * pi
        return self.rotation

    @property
    def shape(self):
        """
        creates vertices for a diamond-ish shape with
        """
        offset = self.scale * 5
        aligner = (3.0 / 4.0) * pi
        return rotate_polygon(
            polygon=[
                (
                    self.x - offset,
                    self.y - offset
                ),
                (
                    self.x,
                    self.y + offset
                ),
                (
                    self.x + offset,
                    self.y + offset
                ),
                (
                    self.x + offset,
                    self.y
                )
            ],
            r=self.rotation + aligner,
            around=self.center
        )


def boids_pygame(world):
    pygame.init()

    window = pygame.display.set_mode(WINDOW_DIMENSIONS)

    while True:
        world.update()

        window.fill(BACKGROUND)

        for boid in world.boids:
            shape = PointyShape(boid.x, boid.y, rotation=boid.heading, color=boid.color)
            pygame.draw.polygon(window, shape.color, shape.shape)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            else:
                print event

        sleep(0.05)