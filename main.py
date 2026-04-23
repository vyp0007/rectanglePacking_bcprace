import time
from placement.otherAlgorithms.bottomLeftFill import bottom_left_fill
from utils import sortInput
from utils.rectangleFileLoader import load_rectangles_from_json
from visualizer import VisualizerApp
import json
from basicComponents.rectangle import Rectangle
from geneticAlgorithms import pygadGenetic, pyswarmsPSO
from basicComponents.rectangleContainer import Container
from utils.stats.experimentTracker import ExperimentTracker
from utils.stats.statVisualizer import ExperimentVisualizer



                    
def place_rectangles_to_container(con : Container,rects : list[Rectangle]):
    for r in rects:
        con.add_rectangle(r)


def build_container_from_solution(solution, rectangles, width):
    sorted_rects = sortInput.sort_with_keys(rectangles, solution)
    return bottom_left_fill(width, sorted_rects)

if __name__ == "__main__":
    width, rectangles = load_rectangles_from_json("problems/mid_256.json")
    config = {"num_generations": 30, "sol_per_pop": 12, "num_parents_mating": 6, "useRTree" : False}
    tracker = ExperimentTracker()
    ga = pygadGenetic.PygadGA(rectangles, width, config, tracker)
    start_time = time.perf_counter()
    ga.run()
    end_time = time.perf_counter()

    print(f"runGA took {end_time - start_time:.6f} seconds")

    tracker.save_csv("./algorithmStats/testStats.csv")
    #ExperimentVisualizer.plot_from_csv("./algorithmStats/testStats.csv")


    generations = ga.ga_instance.best_solutions

    #generations = [solution]
    #testContainer = bottom_left_fill(width,rectangles)

    app = VisualizerApp(
        num_generations=len(generations),
        num_populations=1,
        container_width=width,
        canvas_width=600,
        canvas_height=600,
    )

    def on_gen_changed(gen_idx):
        solution = generations[gen_idx]
        container = build_container_from_solution(solution, rectangles, width)
        app.set_container(container)

    def on_pop_changed(gen_idx, pop_idx):
        solution = generations[gen_idx]
        container = build_container_from_solution(solution, rectangles, width)
        app.set_container(container)

    app.on_generation_changed = on_gen_changed
    app.on_population_changed = on_pop_changed

    # load initial view
    on_gen_changed(0)

    app.run()
