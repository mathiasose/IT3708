from __future__ import print_function, division, unicode_literals
import pygame
from time import sleep
from math import cos, sin, pi

from utils import *


LINE_WIDTH = 1

CELL_SIZE = 50
AGENT_R = CELL_SIZE // 3
EDIBLE_R = CELL_SIZE // 5
ARROW_R = CELL_SIZE // 9

BACKGROUND = (255, 255, 255)
FOREGROUND = (0, 0, 0)

START = (0, 255, 0)
FOOD_COLOR = (0, 125, 0)
POISON_COLOR = (255, 0, 0)
ARROW_COLOR = (0, 0, 0)

SLEEP_TIME_DEFAULT = 0.5
SLEEP_TIME_DELTA = 0.10

TITLE = 'Q-Learning to navigate a Flatland problem'


def rotate_point(point, r, around):
    translated = point[0] - around[0], point[1] - around[1]
    rotated = (translated[0] * cos(r) - translated[1] * sin(r), translated[0] * sin(r) + translated[1] * cos(r))
    reverse_translated = rotated[0] + around[0], rotated[1] + around[1]
    return reverse_translated


def rotate_polygon(polygon, r=0.0, around=(0, 0)):
    if r == 0:
        return polygon

    return [rotate_point(corner, r, around) for corner in polygon]


class PointyShape(object):
    def __init__(self, x, y, radius, rotation=0.0, color=FOREGROUND):
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


class FlatlandGUI:
    def __init__(self, agent, actions):
        """
        takes a fresh board and a list of actions and visualizes
        """
        self.agent = agent
        self.flatland = agent.world
        self.window_w, self.window_h = self.flatland.w * CELL_SIZE, self.flatland.h * CELL_SIZE

        pygame.init()
        sleep_time = SLEEP_TIME_DEFAULT

        self.paused = True
        self.window = pygame.display.set_mode((self.window_w, self.window_h))

        self.pause()

        for action in actions + [NOOP]:
            self.draw_state()

            while self.paused:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.unpause()
                    elif event.type == pygame.KEYDOWN and event.key == pygame.QUIT:
                        return

            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.pause()
                    elif event.key == pygame.K_PLUS:
                        # go faster
                        sleep_time = max(sleep_time - SLEEP_TIME_DELTA, SLEEP_TIME_DELTA)
                    elif event.key == pygame.K_MINUS:
                        # go slower
                        sleep_time += SLEEP_TIME_DELTA

            sleep(sleep_time)
            self.agent.move(action)

        self.finish()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    return

    def draw_state(self):
        self.window.fill(BACKGROUND)

        for x in xrange(self.flatland.w):
            x1 = x * CELL_SIZE - 1
            pygame.draw.line(self.window, FOREGROUND, (x1, 0), (x1, self.window_h), LINE_WIDTH)

        for y in xrange(self.flatland.h):
            y1 = y * CELL_SIZE - 1
            pygame.draw.line(self.window, FOREGROUND, (0, y1), (self.window_w, y1), LINE_WIDTH)

        eaten, pos = self.agent.state
        for y, row in enumerate(self.flatland.grid):
            for x, cell in enumerate(row):
                if (x, y) == self.flatland.agent_initial_position:
                    self.fill_cell(x, y, START)
                if (x, y) == self.agent.position:
                    self.draw_circle_in_cell(x, y, (0, 0, 125), radius=AGENT_R)
                elif is_food(cell):
                    self.draw_circle_in_cell(x, y, FOOD_COLOR, radius=EDIBLE_R)
                elif is_poison(cell):
                    self.draw_circle_in_cell(x, y, POISON_COLOR, radius=EDIBLE_R)
                else:
                    direction = self.agent.best_action(state=(eaten, (x, y)))
                    if direction:
                        self.arrow_in_cell(x, y, direction, ARROW_COLOR)

        pygame.display.flip()

    def draw_circle_in_cell(self, cell_x, cell_y, color, radius=CELL_SIZE // 8):
        offset = CELL_SIZE // 2
        coord = cell_x * CELL_SIZE + offset, cell_y * CELL_SIZE + offset
        pygame.draw.circle(self.window, color, coord, radius)

    def fill_cell(self, cell_x, cell_y, color):
        x, y = cell_x * CELL_SIZE + LINE_WIDTH // 2, cell_y * CELL_SIZE + LINE_WIDTH // 2
        pygame.draw.rect(self.window, color, pygame.Rect(x, y, CELL_SIZE - LINE_WIDTH, CELL_SIZE - LINE_WIDTH))

    def arrow_in_cell(self, cell_x, cell_y, direction, color):
        x, y = cell_x * CELL_SIZE + CELL_SIZE // 2, cell_y * CELL_SIZE + CELL_SIZE // 2
        rot = {
            NORTH: -.5 * pi,
            EAST: 0,
            SOUTH: .5 * pi,
            WEST: pi
        }
        shape = PointyShape(x, y, ARROW_R, rotation=rot[direction]).shape

        pygame.draw.polygon(self.window, color, shape)

    def pause(self):
        self.paused = True
        pygame.display.set_caption("{} - {}".format(TITLE, 'Paused'))

    def unpause(self):
        self.paused = False
        pygame.display.set_caption(TITLE)

    def finish(self):
        pygame.display.set_caption("{} - {}".format(TITLE, 'Finished'))
        print(self.agent.status)
