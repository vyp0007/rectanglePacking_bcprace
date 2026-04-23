import numpy as np
import pyswarms as ps

from placement.bottomLeftFillSortedLists import bottom_left_fill
from utils.sortInput import sort_with_keys
from utils.stats.experimentTracker import ExperimentTracker


class PySwarmsPSO:
    def __init__(self, rectangles, containerWidth, config: dict, store_best_solution_per_gen : bool = True):
        self.rectangles = rectangles
        self.containerWidth = containerWidth
        self.config = config
        self.current_generation = 0
        self.global_best_cost = float("inf")
        self.global_best_stats = None

        self.n_rects = len(rectangles)
        self.tracker : ExperimentTracker = None
        self.best_stats = None
        self.iterCount = 0

        #hyperparameters
        options = {
            "c1": config.get("c1", 1.5),  # cognitive parameter
            "c2": config.get("c2", 1.5),  # social parameter
            "w": config.get("w", 0.7),    # inertia
        }

        self.optimizer = ps.single.GlobalBestPSO(
            n_particles=config.get("n_particles", 20),
            dimensions=self.n_rects,
            options=options,
            bounds=(np.zeros(self.n_rects), np.ones(self.n_rects)),
        )

        self.best_cost = None
        self.best_position = None
        self.best_solutions = []
        self.global_best_sol = None
        self.storeSolutions = store_best_solution_per_gen

    def myFitnessFunc(self, swarm_positions):
        """
        swarm_positions shape: (n_particles, n_rectangles)
        Returns array of costs (container heights)
        """
        costs = []
        new_best_found = False

        for particle in swarm_positions:
            sorted_input = sort_with_keys(self.rectangles, particle)
            cont = bottom_left_fill(self.containerWidth, sorted_input, False)
            density = cont.getDensity()
            height = cont.height
            width = cont.width
            cost = 1000 - density * 1000
            costs.append(cost)
            self.iterCount += 1

            if cost < self.global_best_cost:
                self.global_best_cost = cost
                self.global_best_stats = {
                    "best_score": 1.0 / cost if cost > 0 else 0,
                    "best_height": height,
                    "best_width": width,
                    "best_density": density
                }
                new_best_found = True
                self.global_best_sol = particle.copy()

        
        
        if self.tracker:
            self.tracker.log(
                generation=self.current_generation,
                best_score=self.global_best_stats["best_score"],
                best_height=self.global_best_stats["best_height"],
                best_width=self.global_best_stats["best_width"],
                best_density=self.global_best_stats["best_density"],
            )
        
        if self.storeSolutions and new_best_found:
            self.best_solutions.append(self.global_best_sol.copy())
        
        self.current_generation += 1

        return np.array(costs)

    
    def run(self, tracker=None):
        iters = self.config.get("iters", 50)
        self.tracker = tracker
        self.current_generation = 0

        if self.tracker:
            self.tracker.start()

        cost, pos = self.optimizer.optimize(
            self.myFitnessFunc,
            iters=iters,
            verbose=False
        )
        return {
            "solution": pos,
            "density": self.global_best_stats["best_density"],
            "fitness": 1.0 / cost,
            "height": self.global_best_stats["best_height"]
        }

