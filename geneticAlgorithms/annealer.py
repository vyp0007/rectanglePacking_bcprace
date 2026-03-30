from simanneal import Annealer
import random
import math
from placement.bottomLeftFillSortedLists import bottom_left_fill
#from placement.otherAlgorithms.PositionsBLF import bottom_left_fill
from utils.sortInput import sort_with_keys



class PackingAnnealer(Annealer):
    def __init__(self, state, rectangles, containerWidth, tracker=None, config=None):
        self.rectangles = rectangles
        self.containerWidth = containerWidth
        self.tracker = tracker
        self.config = config or {}
        self.iteration = 0
        self.solution_history = []

        super().__init__(state)

    def energy(self):
        #sorted_input = sort_with_keys(self.rectangles, self.state)
        sorted_input = [self.rectangles[i] for i in self.state]
        cont = bottom_left_fill(self.containerWidth, sorted_input, optimised=False)
        return 1000 - cont.getDensity() * 1000

    """
    def move(self):
        i = random.randrange(len(self.state))
        self.state[i] += random.uniform(-0.1, 0.1)
        self.state[i] = max(0.0, min(1.0, self.state[i]))
        """

    def move(self):
        i, j = random.sample(range(len(self.state)), 2)
        self.state[i], self.state[j] = self.state[j], self.state[i]

    def update(self, step, T, E, acceptance, improvement):
        if improvement:
            self.solution_history.append(self.best_state.copy())
        if not self.tracker:
            return
        self.tracker.log(
            generation=step,
            best_score=1.0 / self.best_energy if self.best_energy > 0 else 0,
            best_height=self.best_energy
        )
        print("step: ",step," complete")