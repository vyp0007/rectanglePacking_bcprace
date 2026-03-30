import time
from geneticAlgorithms.simannealSA import SimulatedAnnealing
from utils.stats.experimentTracker import ExperimentTracker
from utils.stats.statVisualizer import ExperimentVisualizer
from utils.rectangleFileLoader import load_rectangles_from_json
from visualizer import VisualizerApp
from placement.otherAlgorithms.bottomLeftFill import bottom_left_fill



def build_container_from_solution(solution, rectangles, width):
    sorted_rects = [rectangles[i] for i in solution]
    return bottom_left_fill(width, sorted_rects)

if __name__ == "__main__":

    width, rectangles = load_rectangles_from_json("problems/mid_256.json")

    config = {
        "Tmax": 800,
        "Tmin": 10,
        "steps": 4000
    }

    tracker = ExperimentTracker()

    sa = SimulatedAnnealing(rectangles, width, config, tracker)

    start_time = time.perf_counter()
    result = sa.run()
    end_time = time.perf_counter()

    print(f"runSA took {end_time - start_time:.6f} seconds")

    tracker.save_csv("./algorithmStats/testStatsSA.csv")
    ExperimentVisualizer.plot_from_csv("./algorithmStats/testStatsSA.csv")

    generations = sa.annealer.solution_history

    if not generations:
        generations = [result["solution"]]

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
