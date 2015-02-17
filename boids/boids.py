from __future__ import print_function, division, unicode_literals
from collections import defaultdict
from random import randint, uniform

from config import *
from geometry import euclidean_distance, normalize_vector, angle, point_within_circle


class CartesianWorldObject(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def position(self):
        return self.x, self.y


class Boid(CartesianWorldObject):
    def __init__(self, x, y, vx, vy, world):
        super(Boid, self).__init__(x, y)
        self.vx = vx
        self.vy = vy
        self.world = world
        self.next_x = x
        self.next_y = y
        self.max_speed = BOID_MAX_SPEED
        self.dead = False
        self.avoiding = False
        self.fleeing = False

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
        """
        With the world wrapping left<->right and top<->down there is 4 possible vectors from point a to point b,
        this returns the shortest.
        """
        x1 = other_x - self.x
        x_sign = 0 if x1 == 0 else (x1 // abs(x1))
        x2 = -x_sign * (self.world.width - abs(x1))

        y1 = other_y - self.y
        y_sign = 0 if y1 == 0 else (y1 // abs(y1))
        y2 = -y_sign * (self.world.height - abs(y1))

        return min(x1, x2, key=abs), min(y1, y2, key=abs)

    def shortest_distance(self, x, y):
        """
        The magnitude of the relative coordinate vector.
        """
        return euclidean_distance((0, 0), self.relative_coordinates(x, y))

    # def course_adjusting_force(self, target_vx, target_vy):
    #     dx = target_vx - self.vx
    #     dy = target_vy - self.vy
    #     return dx, dy

    @property
    def neighbours(self):
        """
        The set of other boids that are within "sight" of this boid (excluding itself)
        """
        return self.world.neighbour_sets[self]

    @property
    def predators(self):
        """
        The set of predators that are within "sight" of this boid
        """
        return self.world.predator_sets[self]

    def distance(self, other):
        """
        The distance between this boid and another boid/predator __in the neighbourhood__.
        """
        return self.world.distances[self, other]

    def calculate_forces(self):
        """
        The force calculations have been joined into a single function for performance reasons.
        """
        forces = {
            'separation': (0, 0),
            'alignment': (0, 0),
            'cohesion': (0, 0),
            'avoidance': (0, 0),
            'flight': (0, 0)
        }

        self.fleeing = False
        flight_x, flight_y = 0.0, 0.0
        for predator in self.predators:
            self.fleeing = True
            distance = self.distance(predator)
            if distance < PREDATOR_RADIUS:
                dead = self.die()
                if dead:
                    return forces

            factor = 1 - distance / self.world.neighbourhood_radius

            rel_x, rel_y = self.relative_coordinates(predator.x, predator.y)

            flight_x -= factor * rel_x
            flight_y -= factor * rel_y

        forces['flight'] = (flight_x, flight_y)

        self.avoiding = False
        avoidance_x, avoidance_y = 0.0, 0.0
        for obstacle in self.world.obstacles:
            distance = self.shortest_distance(obstacle.x, obstacle.y)
            if distance < (BOID_RADIUS + self.world.neighbourhood_radius + OBSTACLE_RADIUS):
                if distance < OBSTACLE_RADIUS:
                    dead = self.die()
                    if dead:
                        return forces

                normalized_vx, normalized_vy = self.normalized_velocity

                intersection = False
                for n in xrange(1, int(distance)):
                    future_x = self.x + n * normalized_vx
                    future_y = self.y + n * normalized_vy

                    d = euclidean_distance((future_x, future_y), obstacle.position)

                    if d < (obstacle.r + BOID_RADIUS):
                        intersection = True
                        break

                if intersection:
                    self.avoiding = True
                    factor = 1 - (distance - obstacle.r) / self.world.neighbourhood_radius
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

        if len(self.neighbours) == 0:
            return forces

        sum_x, sum_y = 0.0, 0.0
        sum_vx, sum_vy = 0.0, 0.0

        sep_x, sep_y = 0.0, 0.0

        for boid in self.neighbours:
            distance = self.world.distances[self, boid]
            factor = 1 - distance / self.world.neighbourhood_radius
            nvx, nvy = boid.normalized_velocity
            sum_vx += nvx
            sum_vy += nvy

            sum_x += boid.x
            sum_y += boid.y

            rel_x, rel_y = normalize_vector(*self.relative_coordinates(boid.x, boid.y))
            sep_x -= factor * rel_x
            sep_y -= factor * rel_y

        forces['separation'] = (sep_x, sep_y)

        forces['alignment'] = normalize_vector(sum_vx, sum_vy)

        avg_x = sum_x / len(self.neighbours)
        avg_y = sum_y / len(self.neighbours)
        forces['cohesion'] = normalize_vector(*self.relative_coordinates(avg_x, avg_y))

        return forces

    def change_velocity(self):
        if self.dead:
            return

        forces = self.calculate_forces()

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
        if self.velocity_magnitude > self.max_speed:
            norm_x, norm_y = self.normalized_velocity
            self.vx = self.max_speed * norm_x
            self.vy = self.max_speed * norm_y

    def calculate_move(self):
        """
        Calculates the next position of the boid.
        If it passes out of bounds the position will wrap around to the other side.
        """
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
        if ENABLE_DEATH:
            self.dead = True

        return self.dead


class Obstacle(CartesianWorldObject):
    def __init__(self, x, y, r):
        super(Obstacle, self).__init__(x, y)
        self.r = r

    def point_within(self, x, y):
        return point_within_circle((x, y), self.position, self.r)


class Predator(Boid):
    def __init__(self, *args, **kwargs):
        super(Predator, self).__init__(*args, **kwargs)
        self.max_speed = PREDATOR_MAX_SPEED

    def calculate_forces(self):
        preys = self.world.prey_sets[self]

        chase_x, chase_y = 0.0, 0.0
        for boid in preys:
            distance = self.world.distances[self, boid]
            factor = 1 - distance / self.world.neighbourhood_radius
            dir_x, dir_y = normalize_vector(*self.relative_coordinates(boid.x, boid.y))

            chase_x += factor * dir_x
            chase_y += factor * dir_y

        return {
            'chase': normalize_vector(chase_x, chase_y)
        }

    def change_velocity(self):
        if self.dead:
            return

        chase_x, chase_y = self.calculate_forces()['chase']

        self.vx += self.world.chase_weight * chase_x
        self.vy += self.world.chase_weight * chase_y


class BoidWorld(object):
    def __init__(self, dimensions):
        self.scenario = 0
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

        self.tick = TICK
        self.paused = True

        self.neighbour_sets = defaultdict(set)
        self.prey_sets = defaultdict(set)
        self.predator_sets = defaultdict(set)
        self.distances = defaultdict(int)

        self.neighbourhood_radius = NEIGHBOURHOOD_RADIUS

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
        for creature in self.creatures:
            if creature.position == (x, y):
                return True

        for obstacle in self.obstacles:
            if obstacle.point_within(x, y):
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

            vx = uniform(-1, 1) * PREDATOR_MAX_SPEED
            vy = uniform(-1, 1) * PREDATOR_MAX_SPEED
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

    def clear_predators(self):
        self.predators = []

    def resurrect_boids(self):
        for boid in self.boids:
            boid.dead = False

    def set_distance(self, a, b, distance):
        """
        Sets the distance with both key permutations
        """
        self.distances[a, b] = self.distances[b, a] = distance

    def find_neighbours(self):
        """
        This logic was moved out of the Boid/Predator classes
        in order to optimize for performance
        """
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
                    self.set_distance(boid, other_boid, distance)

            for predator in self.predators:
                distance = boid.shortest_distance(predator.x, predator.y)

                if distance <= self.neighbourhood_radius:
                    self.predator_sets[boid].add(predator)
                    self.prey_sets[predator].add(boid)
                    self.set_distance(boid, predator, distance)
