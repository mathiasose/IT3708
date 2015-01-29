from math import atan2
from random import randint, uniform

from config import *
from geometry import euclidean_distance, normalize_vector
from gui import random_color


class Boid(object):
    def __init__(self, x, y, vx, vy, world):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.world = world
        self.color = random_color()
        self.next_x = x
        self.next_y = y

    @property
    def position(self):
        return self.x, self.y

    @property
    def velocity(self):
        return self.vx, self.vy

    @property
    def velocity_magnitude(self):
        return euclidean_distance((0, 0), self.velocity)

    @property
    def normalized_velocity(self):
        return normalize_vector(self.vx, self.vy)

    @property
    def heading(self):
        return atan2(self.vy, self.vx)

    def relative_coordinates(self, x2, y2):
        x1 = self.x
        y1 = self.y
        w = self.world.width
        h = self.world.height

        ax, ay = x2 - x1, y2 - y1
        bx, by = w - abs(ax), h - abs(ay)

        return min(ax, bx, key=abs), min(ay, by, key=abs)

    def shortest_distance(self, x, y):
        return euclidean_distance((0, 0), self.relative_coordinates(x, y))

    @property
    def neighbours(self):
        """
        excludes self
        """
        r = []
        for boid in self.world.boids:
            if boid.position == self.position:
                continue

            distance = self.shortest_distance(boid.x, boid.y) - 2 * BOID_RADIUS

            if distance <= self.world.neighbourhood_radius:
                r.append((boid, distance))

        return r

    def calculate_forces(self):
        neighbours = self.neighbours
        neighbour_count = len(neighbours)

        forces = {
            'separation': (0, 0),
            'alignment': (0, 0),
            'cohesion': (0, 0),
            'avoidance': (0, 0)
        }

        avoidance_x, avoidance_y = 0.0, 0.0
        for obstacle in self.world.obstacles:
            distance = self.shortest_distance(obstacle.x, obstacle.y)
            if distance < (NEIGHBOURHOOD_RADIUS + OBSTACLE_RADIUS + BOID_RADIUS):
                normalized_vx, normalized_vy = self.normalized_velocity

                future_x = distance * normalized_vx + self.x
                future_y = distance * normalized_vy + self.y

                d = euclidean_distance((future_x, future_y), obstacle.position)

                if d < (obstacle.r + BOID_RADIUS):
                    factor = 1 - d / obstacle.r
                    avoidance_x += factor * -normalized_vy
                    avoidance_y += factor * normalized_vx

        forces['avoidance'] = normalize_vector(avoidance_x, avoidance_y)

        if neighbour_count == 0:
            return forces

        sum_x, sum_y = 0.0, 0.0
        sum_vx, sum_vy = 0.0, 0.0

        for boid, distance in neighbours:
            factor = 1 - distance / float(NEIGHBOURHOOD_RADIUS)

            sum_x += factor * boid.x
            sum_y += factor * boid.y
            sum_vx += factor * boid.vx
            sum_vy += factor * boid.vy

        avg_x = sum_x / neighbour_count
        avg_y = sum_y / neighbour_count

        avg_vx = sum_vx / neighbour_count
        avg_vy = sum_vy / neighbour_count

        forces['separation'] = normalize_vector(sum_vx - self.vx, sum_vy - self.vy)
        forces['alignment'] = normalize_vector(avg_vx - self.vx, avg_vy - self.vy)
        forces['cohesion'] = normalize_vector(avg_x - self.vx, avg_y - self.vy)

        return forces

    def change_velocity(self):
        forces = self.calculate_forces()
        separation_x, separation_y = forces['separation']
        alignment_x, alignment_y = forces['alignment']
        cohesion_x, cohesion_y = forces['cohesion']
        avoidance_x, avoidance_y = forces['avoidance']

        self.vx += sum((
            self.world.separation_weight * separation_x,
            self.world.alignment_weight * alignment_x,
            self.world.cohesion_weight * cohesion_x,
            self.world.avoidance_weight * avoidance_x
        ))

        self.vy += sum((
            self.world.separation_weight * separation_y,
            self.world.alignment_weight * alignment_y,
            self.world.cohesion_weight * cohesion_y,
            self.world.avoidance_weight * avoidance_y
        ))

        if self.velocity_magnitude > BOID_MAX_SPEED:
            nx, ny = self.normalized_velocity
            self.vx = BOID_MAX_SPEED * nx
            self.vy = BOID_MAX_SPEED * ny

    def calculate_move(self):
        self.next_x = self.x + int(STEP_SCALE * self.vx)
        self.next_x %= self.world.width

        self.next_y = self.y + int(STEP_SCALE * self.vy)
        self.next_y %= self.world.height

    def do_move(self):
        self.x = self.next_x
        self.y = self.next_y


class Obstacle(object):
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    @property
    def position(self):
        return self.x, self.y


class BoidWorld(object):
    def __init__(self, dimensions, neighbourhood_radius):
        self.scenario = 1
        self.separation_weight = SCENARIOS[self.scenario][0]
        self.alignment_weight = SCENARIOS[self.scenario][1]
        self.cohesion_weight = SCENARIOS[self.scenario][2]
        self.avoidance_weight = OBSTACLE_AVOIDANCE_WEIGHT

        self.dimensions = dimensions

        self.boids = []
        self.neighbourhood_radius = neighbourhood_radius

        self.obstacles = []

        self.tick = TICK
        self.paused = True

    def change_scenario(self, n):
        self.scenario = n
        self.separation_weight = SCENARIOS[self.scenario][0]
        self.alignment_weight = SCENARIOS[self.scenario][1]
        self.cohesion_weight = SCENARIOS[self.scenario][2]

    @property
    def width(self):
        return self.dimensions[0]

    @property
    def height(self):
        return self.dimensions[1]

    def is_occupied(self, x, y):
        for boid in self.boids:
            if boid.position == (x, y):
                return True

        return False

    def add_boids(self, n):
        remaining = n
        while remaining:
            x = randint(0, self.width)
            y = randint(0, self.height)

            if self.is_occupied(x, y):
                continue

            vx = uniform(-1, 1) * (BOID_MAX_SPEED / 2)
            vy = uniform(-1, 1) * (BOID_MAX_SPEED / 2)
            self.boids.append(Boid(x, y, vx, vy, world=self))
            remaining -= 1

        return self.boids

    def add_obstacle(self, x, y, r=OBSTACLE_RADIUS):
        self.obstacles.append(Obstacle(x, y, r))

    def calculate_moves(self):
        for boid in self.boids:
            boid.change_velocity()
            boid.calculate_move()

    def do_moves(self):
        for boid in self.boids:
            boid.do_move()

    def clear_obstacles(self):
        self.obstacles = []
