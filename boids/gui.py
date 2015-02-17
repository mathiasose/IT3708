from __future__ import print_function, division, unicode_literals
from math import pi
from random import randint
import sys
import pygame
from time import sleep

from config import *
from geometry import rotate_polygon, heading


random_color = lambda: (randint(0, 255), randint(0, 255), randint(0, 255))

colors = {}


class PointyShape(object):
    def __init__(self, x, y, radius=BOID_RADIUS, rotation=0.0, color=FOREGROUND):
        self.x = x
        self.y = y
        self.rotation = rotation
        self.color = color
        self.radius = radius

    @property
    def center(self):
        return self.x, self.y

    def rotate(self, dr):
        self.rotation += dr
        self.rotation %= 2 * pi
        return self.rotation

    @property
    def shape(self):
        return rotate_polygon(
            polygon=[
                (
                    self.x - self.radius,
                    self.y - self.radius
                ),
                (
                    self.x,
                    self.y + self.radius
                ),
                (
                    self.x + self.radius,
                    self.y + self.radius
                ),
                (
                    self.x + self.radius,
                    self.y
                )
            ],
            r=self.rotation + (3.0 / 4.0) * pi,
            around=self.center
        )


def keydown_handler(world, event):
    if event.key == pygame.K_q:
        world.separation_weight += ADJUST_WEIGHT
    elif event.key == pygame.K_a:
        world.separation_weight -= ADJUST_WEIGHT
    elif event.key == pygame.K_w:
        world.alignment_weight += ADJUST_WEIGHT
    elif event.key == pygame.K_s:
        world.alignment_weight -= ADJUST_WEIGHT
    elif event.key == pygame.K_e:
        world.cohesion_weight += ADJUST_WEIGHT
    elif event.key == pygame.K_d:
        world.cohesion_weight -= ADJUST_WEIGHT
    elif event.key == pygame.K_r:
        world.neighbourhood_radius += BOID_RADIUS
    elif event.key == pygame.K_f:
        world.neighbourhood_radius -= BOID_RADIUS
        if world.neighbourhood_radius <= 0:
            world.neighbourhood_radius = BOID_RADIUS
    elif event.key == pygame.K_t:
        world.tick += ADJUST_TICK
    elif event.key == pygame.K_g:
        world.tick -= ADJUST_TICK
        if world.tick < 0:
            world.tick = 0
    elif event.key == pygame.K_SPACE:
        world.paused = not world.paused
    elif event.key == pygame.K_0:
        world.change_scenario(0)
    elif event.key == pygame.K_1:
        world.change_scenario(1)
    elif event.key == pygame.K_2:
        world.change_scenario(2)
    elif event.key == pygame.K_3:
        world.change_scenario(3)
    elif event.key == pygame.K_4:
        world.change_scenario(4)
    elif event.key == pygame.K_5:
        world.change_scenario(5)
    elif event.key == pygame.K_6:
        world.change_scenario(6)
    elif event.key == pygame.K_PLUS:
        world.add_boids(1)
    elif event.key == pygame.K_BACKSLASH:
        world.add_predator()
    elif event.key == pygame.K_RETURN:
        world.clear_obstacles()
    elif event.key == pygame.K_BACKSPACE:
        world.clear_predators()
    elif event.key == pygame.K_QUOTE:
        world.resurrect_boids()
    else:
        return

    print("sep: {}\tali: {}\tcoh: {}\tr: {}".format(
        world.separation_weight, world.alignment_weight, world.cohesion_weight, world.neighbourhood_radius
    ))


def run_boids_pygame(world):
    pygame.init()

    window = pygame.display.set_mode(WINDOW_DIMENSIONS)

    # for boid in world.boids:
    # colors[boid] = random_color()

    while True:
        if not world.paused:
            world.find_neighbours()
            world.calculate_moves()
            world.do_moves()

        window.fill(BACKGROUND)

        for obstacle in world.obstacles:
            pygame.draw.circle(window, (255, 255, 255), obstacle.position, obstacle.r)

        for boid in world.boids:
            try:
                colors[boid]
            except KeyError:
                colors[boid] = random_color()

            shape = PointyShape(
                x=boid.x,
                y=boid.y,
                rotation=heading(boid.vx, boid.vy),
                color=(255, 0, 0) if boid.dead else (255, 255, 0) if boid.avoiding or boid.fleeing else FOREGROUND
            )
            pygame.draw.polygon(window, shape.color, shape.shape)

        for predator in world.predators:
            shape = PointyShape(
                x=predator.x,
                y=predator.y,
                rotation=heading(predator.vx, predator.vy),
                color=(255, 0, 0),
                radius=PREDATOR_RADIUS
            )
            pygame.draw.polygon(window, shape.color, shape.shape)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                keydown_handler(world, event)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                world.add_obstacle(x, y)

        sleep(world.tick)
