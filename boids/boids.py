from __future__ import print_function, division, unicode_literals
from collections import defaultdict
from random import randint, uniform

from config import *
from geometry import euclidean_distance, normalize_vector, angle


class Boid(object):
    def __init__(self, x, y, vx, vy, world):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.world = world
        self.next_x = x
        self.next_y = y

        self.dead = False

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
        """
        aka a length 1 vector in the current movement direction
        """
        return normalize_vector(self.vx, self.vy)

    def relative_coordinates(self, other_x, other_y):
        ax, ay = other_x - self.x, other_y - self.y
        bx, by = self.world.width - abs(ax), self.world.height - abs(ay)

        return min(ax, bx, key=abs), min(ay, by, key=abs)

    def shortest_distance(self, x, y):
        return euclidean_distance((0, 0), self.relative_coordinates(x, y))

    def course_adjusting_force(self, target_vx, target_vy):
        dx = target_vx - self.vx
        dy = target_vy - self.vy
        return dx, dy

    def calculate_forces(self):
        neighbour_boids = self.world.neighbour_sets[self]
        neighbour_predators = self.world.predator_sets[self]
        neighbour_count = len(neighbour_boids)

        forces = {
            'separation': (0, 0),
            'alignment': (0, 0),
            'cohesion': (0, 0),
            'avoidance': (0, 0),
            'flight': (0, 0)
        }

        flight_x, flight_y = 0.0, 0.0
        for predator in neighbour_predators:
            distance = self.world.distances[self, predator]
            if distance < PREDATOR_RADIUS:
                self.die()
                return forces

            factor = 1 - distance / float(NEIGHBOURHOOD_RADIUS)

            rel_x, rel_y = self.relative_coordinates(predator.x, predator.y)

            flight_x -= factor * rel_x
            flight_y -= factor * rel_y

        forces['flight'] = (flight_x, flight_y)

        avoidance_x, avoidance_y = 0.0, 0.0
        for obstacle in self.world.obstacles:
            distance = self.shortest_distance(obstacle.x, obstacle.y)
            if distance < (BOID_RADIUS + NEIGHBOURHOOD_RADIUS + OBSTACLE_RADIUS):
                if distance < OBSTACLE_RADIUS:
                    self.die()
                    return forces

                normalized_vx, normalized_vy = self.normalized_velocity

                intersection = 0
                for n in xrange(1, int(distance)):
                    future_x = self.x + n * normalized_vx
                    future_y = self.y + n * normalized_vy

                    d = euclidean_distance((future_x, future_y), obstacle.position)

                    if d < (obstacle.r + BOID_RADIUS):
                        intersection = n
                        break

                if intersection:
                    factor = 1 - float(intersection) / int(distance)
                    future_x = self.x + distance * normalized_vx
                    future_y = self.y + distance * normalized_vy

                    v1 = self.relative_coordinates(*obstacle.position)
                    v2 = self.relative_coordinates(future_x, future_y)
                    a = angle(v1, v2)
                    if a < 0:
                        factor *= -1

                    avoidance_x += factor * -normalized_vy
                    avoidance_y += factor * normalized_vx

        forces['avoidance'] = (avoidance_x, avoidance_y)

        if neighbour_count == 0:
            return forces

        sum_x, sum_y = 0.0, 0.0
        sum_vx, sum_vy = 0.0, 0.0

        sep_x, sep_y = 0.0, 0.0

        for boid in neighbour_boids:
            distance = self.world.distances[self, boid]
            factor = 1 - distance / float(NEIGHBOURHOOD_RADIUS)
            nvx, nvy = normalize_vector(boid.vx, boid.vy)
            sum_vx += factor * nvx
            sum_vy += factor * nvy

            sum_x += boid.x
            sum_y += boid.y

            rel_x, rel_y = normalize_vector(*self.relative_coordinates(boid.x, boid.y))
            sep_x -= factor * rel_x
            sep_y -= factor * rel_y

        forces['separation'] = (sep_x, sep_y)

        avg_vx = sum_vx / neighbour_count
        avg_vy = sum_vy / neighbour_count
        forces['alignment'] = normalize_vector(avg_vx, avg_vy)

        avg_x = sum_x / neighbour_count
        avg_y = sum_y / neighbour_count
        forces['cohesion'] = normalize_vector(*self.relative_coordinates(avg_x, avg_y))

        return forces

    def change_velocity(self):
        if self.dead:
            return

        forces = self.calculate_forces()
        # print(forces)

        separation_x, separation_y = forces['separation']
        alignment_x, alignment_y = forces['alignment']
        cohesion_x, cohesion_y = forces['cohesion']
        avoidance_x, avoidance_y = forces['avoidance']
        flight_x, flight_y = forces['flight']

        self.vx += sum((
            self.world.separation_weight * separation_x,
            self.world.alignment_weight * alignment_x,
            self.world.cohesion_weight * cohesion_x,
            self.world.avoidance_weight * avoidance_x,
            self.world.flight_weight * flight_x
        ))

        self.vy += sum((
            self.world.separation_weight * separation_y,
            self.world.alignment_weight * alignment_y,
            self.world.cohesion_weight * cohesion_y,
            self.world.avoidance_weight * avoidance_y,
            self.world.flight_weight * flight_y
        ))

    def limit_velocity(self):
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
        if self.dead:
            return

        self.x = self.next_x
        self.y = self.next_y

    def die(self):
        if not DEATH:
            return

        self.dead = True


class Obstacle(object):
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    @property
    def position(self):
        return self.x, self.y


class Predator(Boid):
    def calculate_forces(self):
        preys = self.world.prey_sets[self]
        prey_count = len(preys)

        chase_x, chase_y = 0.0, 0.0
        for boid in preys:
            distance = self.world.distances[self, boid]
            factor = 1 - distance / float(NEIGHBOURHOOD_RADIUS)
            dir_x, dir_y = normalize_vector(*self.relative_coordinates(boid.x, boid.y))

            chase_x += factor * dir_x
            chase_y += factor * dir_y

        forces = {
            'chase': (chase_x, chase_y)
        }

        return forces

    def change_velocity(self):
        if self.dead:
            return

        forces = self.calculate_forces()

        chase_x, chase_y = forces['chase']

        self.vx += sum((
            self.world.chase_weight * chase_x,
        ))

        self.vy += sum((
            self.world.chase_weight * chase_y,
        ))


class BoidWorld(object):
    def __init__(self, dimensions, neighbourhood_radius):
        self.scenario = 1
        self.separation_weight = SCENARIOS[self.scenario][0]
        self.alignment_weight = SCENARIOS[self.scenario][1]
        self.cohesion_weight = SCENARIOS[self.scenario][2]
        self.avoidance_weight = OBSTACLE_AVOIDANCE_WEIGHT
        self.chase_weight = CHASE_WEIGHT
        self.flight_weight = FLIGHT_WEIGHT

        self.dimensions = dimensions

        self.boids = []
        self.obstacles = []
        self.predators = []

        self.neighbourhood_radius = neighbourhood_radius

        self.tick = TICK
        self.paused = True

        self.neighbour_sets = defaultdict(set)
        self.prey_sets = defaultdict(set)
        self.predator_sets = defaultdict(set)
        self.distances = defaultdict(int)

    def change_scenario(self, n):
        self.scenario = n
        self.separation_weight = SCENARIOS[self.scenario][0]
        self.alignment_weight = SCENARIOS[self.scenario][1]
        self.cohesion_weight = SCENARIOS[self.scenario][2]

    def random_coordinates(self):
        return randint(0, self.width), randint(0, self.height)

    @property
    def width(self):
        return self.dimensions[0]

    @property
    def height(self):
        return self.dimensions[1]

    @property
    def creatures(self):
        return self.boids + self.predators

    def is_occupied(self, x, y):
        for boid in self.boids:
            if boid.position == (x, y):
                return True

        return False

    def add_boids(self, n):
        remaining = n
        while remaining:
            x, y = self.random_coordinates()

            if self.is_occupied(x, y):
                continue

            vx = uniform(-1, 1) * (BOID_MAX_SPEED / 2)
            vy = uniform(-1, 1) * (BOID_MAX_SPEED / 2)
            self.boids.append(Boid(x, y, vx, vy, world=self))
            remaining -= 1

        return self.boids

    def add_predator(self):
        while True:
            x, y = self.random_coordinates()

            if self.is_occupied(x, y):
                continue

            vx = uniform(-1, 1) * BOID_MAX_SPEED
            vy = uniform(-1, 1) * BOID_MAX_SPEED
            self.predators.append(Predator(x, y, vx, vy, world=self))

            return self.predators

    def add_obstacle(self, x, y, r=OBSTACLE_RADIUS):
        self.obstacles.append(Obstacle(x, y, r))

    def calculate_moves(self):
        for creature in self.creatures:
            creature.change_velocity()
            creature.limit_velocity()
            creature.calculate_move()

    def do_moves(self):
        for creature in self.creatures:
            creature.do_move()

    def clear_obstacles(self):
        self.obstacles = []

    def resurrect_boids(self):
        for boid in self.boids:
            boid.dead = False

    def find_neighbours(self):
        self.neighbour_sets.clear()
        self.prey_sets.clear()
        self.predator_sets.clear()

        done = set()

        for boid in self.boids:
            done.add(boid)

            if boid.dead:
                continue

            for other_boid in self.boids:
                if other_boid in done:
                    continue

                distance = boid.shortest_distance(other_boid.x, other_boid.y)

                if distance <= self.neighbourhood_radius:
                    self.neighbour_sets[boid].add(other_boid)
                    self.neighbour_sets[other_boid].add(boid)
                    self.distances[boid, other_boid] = self.distances[other_boid, boid] = distance

            for predator in self.predators:
                distance = boid.shortest_distance(predator.x, predator.y)

                if distance <= self.neighbourhood_radius:
                    self.predator_sets[boid].add(predator)
                    self.prey_sets[predator].add(boid)
                    self.distances[boid, predator] = self.distances[predator, boid] = distance
