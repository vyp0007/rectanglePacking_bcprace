import time
from placement.bottomLeftFillSortedLists import bottom_left_fill
from placement.RectangleSliding import rectangle_sliding
from utils import sortInput
from utils.rectangleFileLoader import load_rectangles_from_json
import json
from basicComponents.rectangle import Rectangle
from geneticAlgorithms import pygadGenetic, pyswarmsPSO, pyswarmsPSO_sliding
from basicComponents.rectangleContainer import Container
from utils.stats.experimentTracker import ExperimentTracker
from visualizerImproved import VisualizerApp, AlgorithmVersion


                    
def place_rectangles_to_container(con : Container,rects : list[Rectangle]):
    for r in rects:
        con.add_rectangle(r)


def build_container_from_solution(solution, rectangles, width):
    sorted_rects = sortInput.sort_with_keys(rectangles, solution)
    return bottom_left_fill(width, sorted_rects)


def build_container_from_solution_sliding(solution, rectangles):
    n = len(rectangles)
    rectOrder = solution[:n]
    rectDirs = solution[n:]
    sorted_rects = sortInput.sort_with_keys(rectangles, rectOrder)
    return rectangle_sliding(sorted_rects,rectDirs)

if __name__ == "__main__":
    width, rectangles = load_rectangles_from_json("problems/mid_256.json")
    GAconfig = {"num_generations": 30, "sol_per_pop": 30, "num_parents_mating": 12, "useRTree" : False}
    tracker = ExperimentTracker()
    ga = pygadGenetic.PygadGA(rectangles, width, GAconfig, tracker)
    start_time = time.perf_counter()
    ga.run()
    end_time = time.perf_counter()
    print(f"runGA took {end_time - start_time:.6f} seconds")

    PSOconfig = {
        "iters": 30,
        "n_particles": 30,
        "c1": 1.5,
        "c2": 1.5,
        "w": 0.7,
    }
    pso = pyswarmsPSO.PySwarmsPSO(rectangles,width,PSOconfig)
    start_time = time.perf_counter()
    pso.run()
    end_time = time.perf_counter()
    print(f"run PSO took {end_time - start_time:.6f} seconds")

    PSOslidingConfig = {
        "iters": 5,
        "n_particles": 5,
        "c1": 1.5,
        "c2": 1.5,
        "w": 0.7,
    }
    psoSliding = pyswarmsPSO_sliding.PySwarmsPSO_sliding(rectangles,PSOslidingConfig)
    start_time = time.perf_counter()
    psoSliding.run()
    end_time = time.perf_counter()
    print(f"run PSO took {end_time - start_time:.6f} seconds")
    

    gaGens = ga.ga_instance.best_solutions
    psoGens = pso.best_solutions
    slidingGens = psoSliding.best_solutions
    versions = [AlgorithmVersion("GA",len(gaGens)),AlgorithmVersion("PSO",len(psoGens)),AlgorithmVersion("PSO sliding",len(slidingGens))]
    gensArray = [gaGens,psoGens,slidingGens]

    app = VisualizerApp(versions)

    def on_gen_changed(ver_idx, gen_idx):
        solution = gensArray[ver_idx][gen_idx]
        if ver_idx < 2:
            container = build_container_from_solution(solution, rectangles, width)
        else:
            container = build_container_from_solution_sliding(solution,rectangles)
        app.set_container(container)

    app.on_generation_changed = on_gen_changed

    app.run()
