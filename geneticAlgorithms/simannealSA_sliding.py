from geneticAlgorithms.annealer import PackingAnnealer
import random

from placement.bottomLeftFillSortedLists import bottom_left_fill

class SimulatedAnnealing_Sliding:
    def __init__(self, rectangles, containerWidth, config: dict, tracker=None):
        self.rectangles = rectangles
        self.containerWidth = containerWidth
        self.config = config
        self.tracker = tracker        
        initial_state = {
            "order" : list(range(len(rectangles))),
            "directions" : [random.random() for _ in range(len(rectangles))]
        }
        random.shuffle(initial_state["order"])

        self.annealer = PackingAnnealer(
            initial_state,
            rectangles,
            tracker=tracker,
            config=config
        )

        self.annealer.Tmax = config.get("Tmax", 100.0)
        self.annealer.Tmin = config.get("Tmin", 0.1)
        self.annealer.steps = config.get("steps", 1000)
        #self.annealer.updates = 0

    def run(self):
        if self.tracker:
            self.tracker.start()

        best_state, best_energy = self.annealer.anneal()

        if getattr(self.annealer, "user_exit", False):
            raise KeyboardInterrupt

        self.solution_history = self.annealer.solution_history
        
        return {
            "solution": best_state,
        }