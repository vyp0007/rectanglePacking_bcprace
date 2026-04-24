from geneticAlgorithms.annealer import PackingAnnealer
from geneticAlgorithms.annealer_sliding import PackingAnnealer_Sliding
import random


class SimulatedAnnealing:
    def __init__(self, rectangles, containerWidth, config: dict, use_rectangle_sliding : bool = False, tracker=None):
        self.rectangles = rectangles
        self.containerWidth = containerWidth
        self.config = config
        self.tracker = tracker
        self.best_solutions = []
        if use_rectangle_sliding:
            initial_state = {
                "order" : list(range(len(rectangles))),
                "directions" : [random.random() for _ in range(len(rectangles))]
            }
            random.shuffle(initial_state["order"])
            self.annealer = PackingAnnealer_Sliding(
                initial_state,
                rectangles,
                tracker=tracker,
                config=config
            )

        else:
            initial_state = list(range(len(rectangles)))
            random.shuffle(initial_state)
            self.annealer = PackingAnnealer(
                initial_state,
                rectangles,
                containerWidth,
                tracker=tracker,
                config=config
            )

        self.annealer.Tmax = config.get("Tmax", 100.0)
        self.annealer.Tmin = config.get("Tmin", 0.1)
        self.annealer.steps = config.get("steps", 1000)

    def run(self):
        if self.tracker:
            self.tracker.start()

        best_state, best_energy = self.annealer.anneal()

        if getattr(self.annealer, "user_exit", False):
            raise KeyboardInterrupt

        self.best_solutions = self.annealer.solution_history

        return {
            "solution": best_state,
        }