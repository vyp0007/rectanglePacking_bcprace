from geneticAlgorithms.annealer import PackingAnnealer
import random

from placement.bottomLeftFillSortedLists import bottom_left_fill

class SimulatedAnnealing:
    def __init__(self, rectangles, containerWidth, config: dict, tracker=None):
        self.rectangles = rectangles
        self.containerWidth = containerWidth
        self.config = config
        self.tracker = tracker

        
        #initial_state = [random.random() for _ in rectangles]
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
        #self.annealer.updates = 0  

    def run(self):
        if self.tracker:
            self.tracker.start()

        best_state, best_energy = self.annealer.anneal()

         # detect Ctrl+C
        if getattr(self.annealer, "user_exit", False):
            raise KeyboardInterrupt

        self.solution_history = self.annealer.solution_history

        sorted_rects = [self.rectangles[i] for i in best_state]
        best_cont = bottom_left_fill(self.containerWidth, sorted_rects)

        return {
            "solution": best_state,
            "fitness": 1.0 / best_energy if best_energy > 0 else 0,
            "best_energy": best_energy,
            "height": best_cont.height
        }