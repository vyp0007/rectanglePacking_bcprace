import pygad
#from placement.otherAlgorithms.PositionsBLF import *
from placement.otherAlgorithms.bottomLeftFill import *
from utils.sortInput import sort_with_keys
from placement import bottomLeftFillSortedLists
class PygadGA:
    def __init__(self, rectangles, containerWidth, config: dict, tracker = None):
        self.rectangles = rectangles
        self.containerWidth = containerWidth
        self.config = config
        self.tracker = tracker
        self.useRtreeInPLacement = config.get("useRTree",False)

        self.ga_instance = pygad.GA(
            num_generations=config["num_generations"],
            sol_per_pop=config["sol_per_pop"],
            num_parents_mating=config["num_parents_mating"],
            mutation_probability=config.get("mutation_probability", 0.1),
            crossover_probability=config.get("crossover_probability", 0.9),
            parent_selection_type=config.get("parent_selection_type", "sss"),
            mutation_type=config.get("mutation_type", "random"),
            crossover_type=config.get("crossover_type", "single_point"),
            num_genes=len(self.rectangles),
            fitness_func=self.myFitnessFunc,
            init_range_low=0,
            init_range_high=1,
            save_best_solutions=True,
            on_generation=self.on_generation
        )

    def myFitnessFunc(self, ga_instance, solution, solution_idx):
        sorted_input = sort_with_keys(self.rectangles, solution)
        cont = bottom_left_fill(self.containerWidth, sorted_input, self.useRtreeInPLacement)
        #cont = bottom_left_fill(self.containerWidth, sorted_input, self.useRtreeInPLacement)
        return 1.0 / cont.height
    
    def on_generation(self, ga_instance):
        if not self.tracker:
            return

        fitnesses = ga_instance.last_generation_fitness
        best_fitness = max(fitnesses)

        self.tracker.log(
            generation=ga_instance.generations_completed - 1,
            best_score=best_fitness,
            best_height=1.0 / best_fitness
        )

    def run(self):
        if(self.tracker):
            self.tracker.start()
        self.ga_instance.run()
        solution, fitness, idx = self.ga_instance.best_solution()
        return {
            "solution": solution,
            "fitness": fitness,
            "height": 1.0 / fitness
        }
