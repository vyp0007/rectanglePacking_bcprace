import time
from itertools import product
from geneticAlgorithms import pyswarmsPSO
from utils.rectangleFileLoader import load_rectangles_from_json
from utils.stats.experimentTracker import ExperimentTracker

if __name__ == "__main__":
    width, rectangles = load_rectangles_from_json("problems/mid_256.json")

    c1_values = [1.0, 1.5, 2.0]
    c2_values = [1.0, 1.5, 2.0]
    w_values = [0.5, 0.7, 0.9]


    iters = 100
    n_particles = 50

    for c1, c2, w in product(c1_values, c2_values, w_values):

        config = {
            "iters": iters,
            "n_particles": n_particles,
            "c1": c1,
            "c2": c2,
            "w": w,
        }

        tracker_name = f"PSO_c1={c1}_c2={c2}_w={w}"
        tracker = ExperimentTracker(tracker_name)

        pso = pyswarmsPSO.PySwarmsPSO(rectangles, width, config)

        start_time = time.perf_counter()
        result = pso.run(tracker)
        end_time = time.perf_counter()

        fitness = result["fitness"]
        height = result["height"]

        print(
            f"params: c1={c1}, c2={c2}, w={w} | "
            f"fitness: {fitness:.6f} | height: {height:.2f} | "
            f"time: {end_time - start_time:.2f}s"
        )
        tracker.save_latex(path=f"latex_export/{tracker_name}")
