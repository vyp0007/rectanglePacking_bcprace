import random
import time

from placement.otherAlgorithms.bottomLeftFill import bottom_left_fill
from utils import sortInput
from utils.rectangleFileLoader import load_rectangles_from_json
from visualizer import VisualizerApp
from placement.RectangleSliding import rectangle_sliding
from placement.RectangleSlidingOptimisations import rectangle_sliding as rectangle_sliding_optimised


def build_container_from_solution(solution, rectangles, width):
    sorted_rects = sortInput.sort_with_keys(rectangles, solution)
    return rectangle_sliding(width, sorted_rects)

if __name__ == "__main__":
    width, rectangles = load_rectangles_from_json("problems/large_600.json")

    directions = [random.random() for _ in rectangles]

    app = VisualizerApp(
        num_generations=2,
        num_populations=1,
        container_width=width,
        canvas_width=600,
        canvas_height=600,
    )

    def on_gen_changed(gen_idx):
        #solution =
        if(gen_idx == 0):
            startt = time.perf_counter()
            container = rectangle_sliding_optimised(rectangles,directions)
            endt = time.perf_counter()
            print("optimised took: ",endt-startt)
            app.set_container(container)
        if(gen_idx == 1):
            startt = time.perf_counter()
            container = rectangle_sliding(rectangles,directions)
            endt = time.perf_counter()
            print("regular took: ",endt-startt)
            app.set_container(container)
        

    def on_pop_changed(gen_idx, pop_idx):
        container = rectangle_sliding(rectangles,directions)
        app.set_container(container)

    app.on_generation_changed = on_gen_changed
    app.on_population_changed = on_pop_changed

    # load initial view
    on_gen_changed(0)

    app.run()
