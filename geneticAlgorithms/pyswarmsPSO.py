import numpy as np
import pyswarms as ps

from placement.bottomLeftFillSortedLists import bottom_left_fill
from utils.sortInput import sort_with_keys
from utils.stats.experimentTracker import ExperimentTracker


class PySwarmsPSO:
    def __init__(self, rectangles, containerWidth, config: dict):
        self.rectangles = rectangles
        self.containerWidth = containerWidth
        self.config = config

        self.n_rects = len(rectangles)

        # PSO hyperparameters
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
        self.cost_history = []

    def myFitnessFunc(self, swarm_positions):
        """
        swarm_positions shape: (n_particles, n_rectangles)
        Returns array of costs (container heights)
        """
        costs = []

        for particle in swarm_positions:
            sorted_input = sort_with_keys(self.rectangles, particle)
            cont = bottom_left_fill(self.containerWidth, sorted_input, False)

            costs.append(cont.height)

        return np.array(costs)

    
    def run(self, tracker=None):
        iters = self.config.get("iters", 50)

        if tracker:
            tracker.start()

        cost, pos = self.optimizer.optimize(
            self.myFitnessFunc,
            iters=iters,
            verbose=False
        )

        self.best_cost = cost
        self.best_position = pos

        for i, c in enumerate(self.optimizer.cost_history):
            if tracker:
                tracker.log(
                    generation=i,
                    best_score=1.0 / c,
                    best_height=c
                )

        return {
            "solution": pos,
            "fitness": 1.0 / cost,
            "height": cost
        }

    """
    def run(self, tracker=None):
        iters = self.config.get("iters", 50)

        if tracker:
            tracker.start()

        for i in range(iters):
            cost, pos = self.optimizer.optimize(
                self.myFitnessFunc,
                iters=1,
                verbose=False
            )

            self.best_cost = cost
            self.best_position = pos

            if tracker:
                tracker.log(
                    generation=i,
                    best_score=1.0 / cost,
                    best_height=cost
                )

        return {
            "solution": self.best_position,
            "fitness": 1.0 / self.best_cost,
            "height": self.best_cost
        }
    """