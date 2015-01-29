from boids import BoidWorld
from config import *
from gui import boids_pygame

if __name__ == "__main__":
    world = BoidWorld(
        dimensions=WINDOW_DIMENSIONS,
        neighbourhood_radius=NEIGHBOURHOOD_RADIUS
    )

    world.add_boids(NUMBER_OF_BOIDS)

    boids_pygame(world)