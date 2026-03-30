import numpy as np
import pyswarms as ps

from placement.RectangleSliding import rectangle_sliding
from utils.sortInput import sort_with_keys
from utils.stats.experimentTracker import ExperimentTracker


class PySwarmsPSO:
    def __init__(self, rectangles, containerWidth, config: dict):
        self.rectangles = rectangles
        self.containerWidth = containerWidth
        self.config = config

        self.n_genes = len(rectangles) * 2

        # PSO hyperparameters
        options = {
            "c1": config.get("c1", 1.5),  # cognitive parameter
            "c2": config.get("c2", 1.5),  # social parameter
            "w": config.get("w", 0.7),    # inertia
        }

        self.optimizer = ps.single.GlobalBestPSO(
            n_particles=config.get("n_particles", 20),
            dimensions=self.n_genes,
            options=options,
            bounds=(np.zeros(self.n_genes), np.ones(self.n_genes)),
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
        n = len(self.rectangles)
       

        for particle in swarm_positions:
            rectOrder = particle[:n]
            rectDirs = particle[n:]
            sorted_input = sort_with_keys(self.rectangles, rectOrder)
            cont = rectangle_sliding(sorted_input,rectDirs)

            costs.append(cont.height + cont.width)

        print("GEN COMPLETE")

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