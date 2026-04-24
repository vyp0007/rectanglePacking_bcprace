import time
from placement.bottomLeftFillSortedLists import bottom_left_fill
from placement.RectangleSliding import rectangle_sliding
from utils import sortInput
from utils.rectangleFileLoader import load_rectangles_from_json
import json
from basicComponents.rectangle import Rectangle
from geneticAlgorithms import pygadGenetic, pyswarmsPSO, pyswarmsPSO_sliding, pygadGenetic_sliding, simannealSA_sliding, simannealSA
from basicComponents.rectangleContainer import Container
from utils.stats.experimentTracker import ExperimentTracker
from visualizerImproved import VisualizerApp, AlgorithmVersion


                    
def place_rectangles_to_container(con : Container,rects : list[Rectangle]):
    for r in rects:
        con.add_rectangle(r)


def build_container_from_solution(solution, rectangles, width):
    sorted_rects = sortInput.sort_with_keys(rectangles, solution)
    return bottom_left_fill(width, sorted_rects)


def build_container_from_solution_SA(solution, rectangles, width):
    rectOrder = solution
    sorted_rects = [rectangles[i] for i in rectOrder]
    return bottom_left_fill(width, sorted_rects)

def build_container_from_solution_SA_sliding(solution, rectangles):
    rectOrder = solution["order"]
    rectDirs = solution["directions"]
    sorted_rects = [rectangles[i] for i in rectOrder]
    return rectangle_sliding(sorted_rects,rectDirs)


def build_container_from_solution__sliding(solution, rectangles):
    n = len(rectangles)
    rectOrder = solution[:n]
    rectDirs = solution[n:]
    sorted_rects = sortInput.sort_with_keys(rectangles, rectOrder)
    return rectangle_sliding(sorted_rects,rectDirs)

if __name__ == "__main__":
    width, rectangles = load_rectangles_from_json("problems/mid_256.json")
    """
    GAconfig = {"num_generations": 10, "sol_per_pop": 30, "num_parents_mating": 12, "useRTree" : False}
    tracker = ExperimentTracker()
    ga = pygadGenetic.PygadGA(rectangles, width, GAconfig, tracker)
    start_time = time.perf_counter()
    ga.run()
    end_time = time.perf_counter()
    print(f"runGA took {end_time - start_time:.6f} seconds")

    PSOconfig = {
        "iters": 30,
        "n_particles": 10,
        "c1": 1.5,
        "c2": 1.5,
        "w": 0.7,
    }
    pso = pyswarmsPSO.PySwarmsPSO(rectangles,width,PSOconfig)
    start_time = time.perf_counter()
    pso.run()
    end_time = time.perf_counter()
    print(f"run PSO took {end_time - start_time:.6f} seconds")

    PSOslidingConfig = {"iters": 5,"n_particles": 5,"c1": 1.5,"c2": 1.5,"w": 0.7,    }
    psoSliding = pyswarmsPSO_sliding.PySwarmsPSO_sliding(rectangles,PSOslidingConfig)
    start_time = time.perf_counter()
    psoSliding.run()
    end_time = time.perf_counter()
    print(f"run PSO took {end_time - start_time:.6f} seconds")
    
    pygaDslidingConfig = {"num_generations": 2, "sol_per_pop": 4, "num_parents_mating": 3, "useRTree" : False}
    pygaDsliding = pygadGenetic_sliding.PygadGA_sliding(rectangles,pygaDslidingConfig)
    start_time = time.perf_counter()
    pygaDsliding.run()
    end_time = time.perf_counter()
    print(f"run GA sliding took {end_time - start_time:.6f} seconds")
        """
    SAconfig = { "Tmax": 800, "Tmin": 10, "steps": 500 }

    sa = simannealSA.SimulatedAnnealing(rectangles,width,SAconfig)

    start_time = time.perf_counter()
    result = sa.run()
    end_time = time.perf_counter()
    print(f"run SA took {end_time - start_time:.6f} seconds")

    SAconfig_sliding = { "Tmax": 800, "Tmin": 10, "steps": 40 }
    sa_sliding = simannealSA.SimulatedAnnealing(rectangles,width,SAconfig_sliding,True)

    start_time = time.perf_counter()
    result = sa_sliding.run()
    end_time = time.perf_counter()
    print(f"run SA sliding sliding took {end_time - start_time:.6f} seconds")


    #gaGens = ga.best_solutions
    #psoGens = pso.best_solutions
    #slidingGens = pygaDsliding.best_solutions
    saGens = sa.best_solutions
    saSlideGens = sa_sliding.best_solutions
    versions = []
    #versions.append(AlgorithmVersion("GA",len(gaGens)))
    #versions.append(AlgorithmVersion("PSO",len(psoGens)))
    #versions.append(AlgorithmVersion("GA sliding",len(slidingGens)))
    versions.append(AlgorithmVersion("SA",len(saGens)))
    versions.append(AlgorithmVersion("SA sliding",len(saSlideGens)))
    gensArray = [saGens,saSlideGens]

    app = VisualizerApp(versions)

    def on_gen_changed(ver_idx, gen_idx):
        solution = gensArray[ver_idx][gen_idx]
        if ver_idx < 1:
            container = build_container_from_solution_SA(solution, rectangles, width)
        else:
            container = build_container_from_solution_SA_sliding(solution, rectangles)
        app.set_container(container)

    app.on_generation_changed = on_gen_changed

    app.run()
