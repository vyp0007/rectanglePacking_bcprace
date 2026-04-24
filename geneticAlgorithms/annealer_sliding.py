import copy

from simanneal import Annealer
import random
import math
from utils.sortInput import sort_with_keys
from placement.RectangleSliding import rectangle_sliding



class PackingAnnealer_Sliding(Annealer):
    def __init__(self, state, rectangles, tracker=None, config=None):
        self.rectangles = rectangles
        self.tracker = tracker
        self.config = config or {}
        self.iteration = 0
        self.solution_history = []
        self.lastContainer = None
        self.last_best_energy = float("inf")
        self.last_energy= None
        

        super().__init__(state)

    def energy(self):
        order = self.state["order"]
        directions = self.state["directions"]
        sorted_input = [self.rectangles[i] for i in order]
        cont = rectangle_sliding(sorted_input,directions)
        self.lastContainer = cont
        self.iteration += 1
        en = 1000 - cont.getDensity() * 1000
        self.last_energy = en
        return en

    """
    def move(self):
        i = random.randrange(len(self.state))
        self.state[i] += random.uniform(-0.1, 0.1)
        self.state[i] = max(0.0, min(1.0, self.state[i]))
        """

    
    def move(self):
        order = self.state["order"]
        directions = self.state["directions"]

        i = 0
        while i < len(order) - 1:
            if random.random() < 0.5:
                #swap adjacent
                order[i], order[i + 1] = order[i + 1], order[i]

                # update directions for both swapped items
                directions[i] = random.random()
                directions[i + 1] = random.random()

                i += 2  #alredy swapper
            else:
                i += 1


    def update(self, step, T, E, acceptance, improvement):
        if E < self.last_best_energy:
            self.last_best_energy = E
            self.solution_history.append(copy.deepcopy(self.state))
        if not self.tracker:
            return
        self.tracker.log(
            generation=step,
            best_score=1000/self.last_energy,
            best_height=self.lastContainer.height,
            best_width=self.lastContainer.width,
            best_density=self.lastContainer.getDensity()
        )
        #print("step: ",step," complete")