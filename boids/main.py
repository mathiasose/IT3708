from boids import BoidWorld
from gui import WINDOW_DIMENSIONS, boids_pygame

if __name__ == "__main__":
    world = BoidWorld(
        dimensions=WINDOW_DIMENSIONS,
        separation_weight=1,
        alignment_weight=1,
        cohesion_weight=1,
        neighbourhood_radius=10
    )

    world.add_boids(1000)

    boids_pygame(world)