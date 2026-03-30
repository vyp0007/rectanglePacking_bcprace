
import time
from geneticAlgorithms import pyswarmsPSO
from main import build_container_from_solution
from placement.otherAlgorithms.bottomLeftFill import bottom_left_fill
from utils import sortInput
from utils.rectangleFileLoader import load_rectangles_from_json
from utils.stats.experimentTracker import ExperimentTracker
from visualizer import VisualizerApp

def build_container_from_solution(solution, rectangles, width):
    sorted_rects = sortInput.sort_with_keys(rectangles, solution)
    return bottom_left_fill(width, sorted_rects)


if __name__ == "__main__":
    width, rectangles = load_rectangles_from_json("problems/mid_256.json")
    tracker = ExperimentTracker()

    config = {
        "iters": 50,
        "n_particles": 30,
        "c1": 1.5,
        "c2": 1.5,
        "w": 0.7,
    }

    pso = pyswarmsPSO.PySwarmsPSO(rectangles, width, config)
    

    start_time = time.perf_counter()
    result = pso.run(tracker)
    end_time = time.perf_counter()

    solution = result["solution"]
    

    print("SOLUTION: ",solution)
    print(f"runPSO took {end_time - start_time:.6f} seconds")
    print("Best height:", result["height"])

    app = VisualizerApp(
        num_generations=1,
        num_populations=1,
        container_width=width,
        canvas_width=600,
        canvas_height=600,
    )

    def on_gen_changed(gen_idx):
        #solution = result
        container = build_container_from_solution(solution, rectangles, width)
        app.set_container(container)

    def on_pop_changed(gen_idx, pop_idx):
        #solution = result
        container = build_container_from_solution(solution, rectangles, width)
        app.set_container(container)

    app.on_generation_changed = on_gen_changed
    app.on_population_changed = on_pop_changed

    # load initial view
    on_gen_changed(0)

    app.run()
