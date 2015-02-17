from boids import BoidWorld
from config import *
from gui import run_boids_pygame

if __name__ == "__main__":
    boid_world = BoidWorld(dimensions=WINDOW_DIMENSIONS)
    boid_world.add_obstacle(WINDOW_DIMENSIONS[0] / 2, WINDOW_DIMENSIONS[1] / 2)
    boid_world.add_boids(NUMBER_OF_BOIDS)
    run_boids_pygame(boid_world)
