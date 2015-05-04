from __future__ import print_function, division, unicode_literals
import pygame
from time import sleep

from utils import *


LINE_WIDTH = 2

CELL_SIZE = 50
BACKGROUND = (255, 255, 255)
FOREGROUND = (0, 0, 0)

START = (0, 255, 0)
FOOD_COLOR = (0, 125, 0)
POISON_COLOR = (125, 0, 0)

SLEEP_TIME_DEFAULT = 1.0
SLEEP_TIME_DELTA = 0.25

TITLE = ''


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
                if event.type == pygame.QUIT:
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

        pygame.display.set_caption("{} - {}".format(TITLE, 'Finished'))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

    def draw_state(self):
        self.window.fill(BACKGROUND)

        for x in xrange(self.flatland.w):
            x1 = x * CELL_SIZE - 1
            pygame.draw.line(self.window, FOREGROUND, (x1, 0), (x1, self.window_h), LINE_WIDTH)

        for y in xrange(self.flatland.h):
            y1 = y * CELL_SIZE - 1
            pygame.draw.line(self.window, FOREGROUND, (0, y1), (self.window_w, y1), LINE_WIDTH)

        for y, row in enumerate(self.flatland.grid):
            for x, cell in enumerate(row):
                if (x, y) == self.flatland.agent_initial_position:
                    self.fill_cell(x, y, START)
                if (x, y) == self.agent.position:
                    self.draw_circle_in_cell(x, y, (0, 0, 125), radius=CELL_SIZE // 4)
                elif is_food(cell):
                    self.draw_circle_in_cell(x, y, FOOD_COLOR, radius=CELL_SIZE // 5)
                elif is_poison(cell):
                    self.draw_circle_in_cell(x, y, POISON_COLOR)

        pygame.display.flip()

    def draw_circle_in_cell(self, cell_x, cell_y, color, radius=CELL_SIZE // 8):
        offset = CELL_SIZE // 2
        coord = cell_x * CELL_SIZE + offset, cell_y * CELL_SIZE + offset
        pygame.draw.circle(self.window, color, coord, radius)

    def fill_cell(self, cell_x, cell_y, color):
        x, y = cell_x * CELL_SIZE + LINE_WIDTH // 2, cell_y * CELL_SIZE + LINE_WIDTH // 2
        pygame.draw.rect(self.window, color, pygame.Rect(x, y, CELL_SIZE - LINE_WIDTH, CELL_SIZE - LINE_WIDTH))

    def pause(self):
        self.paused = True
        pygame.display.set_caption("{} - {}".format(TITLE, 'Paused'))

    def unpause(self):
        self.paused = False
        pygame.display.set_caption(TITLE)
