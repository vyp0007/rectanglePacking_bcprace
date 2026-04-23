import numpy as np
import pygad
#from placement.otherAlgorithms.PositionsBLF import *
#from placement.otherAlgorithms.bottomLeftFill import *
from utils.sortInput import sort_with_keys
from placement.RectangleSliding import rectangle_sliding

class PygadGA_sliding:
    def __init__(self, rectangles, config: dict, tracker = None, store_best_solutions_per_gen : bool = True ):
        self.rectangles = rectangles
        self.config = config
        self.tracker = tracker
        self.useRtreeInPLacement = config.get("useRTree",False)
        self._containers_cache = {}
        self.best_solutions = []
        self.global_best_fittness = 0.0
        self.store_best_solutions = store_best_solutions_per_gen
        self.ga_instance = pygad.GA(
            num_generations=config["num_generations"],
            sol_per_pop=config["sol_per_pop"],
            num_parents_mating=config.get("num_parents_mating",config["sol_per_pop"] // 2),
            mutation_probability=config.get("mutation_probability", 0.1),
            crossover_probability=config.get("crossover_probability", 0.9),
            parent_selection_type=config.get("parent_selection_type", "sss"),
            mutation_type=config.get("mutation_type", "random"),
            crossover_type=config.get("crossover_type", "single_point"),
            num_genes=len(self.rectangles) * 2,
            fitness_func=self.myFitnessFunc,
            init_range_low=0,
            init_range_high=1,
            save_best_solutions=False,
            on_generation=self.on_generation
        )

    def myFitnessFunc(self, ga_instance, solution, solution_idx):
        n = len(self.rectangles)   
        rectOrder = solution[:n]
        rectDirs = solution[n:]
        sorted_input = sort_with_keys(self.rectangles, rectOrder)
        cont = rectangle_sliding(sorted_input,rectDirs)
        if self.tracker:
            self._containers_cache[solution_idx] = cont

        return cont.getDensity()
    
    def on_generation(self, ga_instance):        

        fitnesses = ga_instance.last_generation_fitness
        best_idx = np.argmax(fitnesses)
        best_fitness = fitnesses[best_idx]
        if self.global_best_fittness < best_fitness:
            self.global_best_fittness = best_fitness
            if self.store_best_solutions:
                bestSolGlobal, bestFitGlobal, idxBestGlobal = ga_instance.best_solution()
                self.best_solutions.append(bestSolGlobal.copy())

        if not self.tracker:
            return
        
        best_cont = self._containers_cache.get(best_idx)
        self.tracker.log(
            generation=ga_instance.generations_completed - 1,
            best_score=best_fitness,
            best_density=1.0 / best_fitness,
            best_height=best_cont.height if best_cont else None,
            best_width=best_cont.width if best_cont else None,
        )
        self._containers_cache.clear()

    def run(self):
        if(self.tracker):
            self.tracker.start()
        self.ga_instance.run()
        solution, fitness, idx = self.ga_instance.best_solution()
        return {
            "solution": solution,
            "fitness": fitness,
            "density": fitness
        }
