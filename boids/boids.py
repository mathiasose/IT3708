from math import sqrt, atan2
from random import random, randint

from gui import random_color


euclidean_distance = lambda a, b: sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

MOVEMENT_FACTOR = 10


class Boid(object):
    def __init__(self, x, y, vx, vy, world):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.world = world
        self.color = random_color()

    @property
    def position(self):
        return self.x, self.y

    @property
    def velocity(self):
        return self.vx, self.vy

    @property
    def heading(self):
        return atan2(self.vy, self.vx)

    @property
    def neighbours(self):
        return [b for b in self.world.boids if
                euclidean_distance(self.position, b.position) <= self.world.neighbourhood_radius]

    @property
    def separation_force(self):
        return self.world.separation_weight * 1, self.world.separation_weight * 1

    @property
    def alignment_force(self):
        return self.world.alignment_weight * 1, self.world.alignment_weight * 1

    @property
    def cohesion_force(self):
        return self.world.cohesion_weight * 1, self.world.cohesion_weight * 1

    def change_velocity(self):
        separation_force = self.separation_force
        alignment_force = self.alignment_force
        cohesion_force = self.cohesion_force

        # self.vx += separation_force[0] + alignment_force[0] + cohesion_force[0]
        # self.vy += separation_force[1] + alignment_force[1] + cohesion_force[1]
        return self.velocity

    def move(self):
        self.x += self.vx
        if self.x > self.world.dimensions[0]:
            self.x -= self.world.dimensions[0]

        self.y += self.vy
        if self.y > self.world.dimensions[1]:
            self.y -= self.world.dimensions[1]

        return self.position


class BoidWorld(object):
    def __init__(self, dimensions, separation_weight, alignment_weight, cohesion_weight, neighbourhood_radius):
        self.dimensions = dimensions

        self.boids = []

        self.separation_weight = separation_weight
        self.alignment_weight = alignment_weight
        self.cohesion_weight = cohesion_weight

        self.neighbourhood_radius = neighbourhood_radius

    def is_occupied(self, x, y):
        for boid in self.boids:
            if boid.position == (x, y):
                return True

        return False

    def add_boids(self, n):
        remaining = n
        while remaining:
            x = randint(0, self.dimensions[0])
            y = randint(0, self.dimensions[1])

            if self.is_occupied(x, y):
                continue

            self.boids.append(
                Boid(x, y, MOVEMENT_FACTOR * (2 * random() - 1), MOVEMENT_FACTOR * (2 * random()) - 1, world=self)
            )
            remaining -= 1

        return self.boids

    def update(self):
        for boid in self.boids:
            boid.change_velocity()
            boid.move()
