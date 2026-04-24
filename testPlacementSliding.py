import random
import time

from placement.otherAlgorithms.bottomLeftFill import bottom_left_fill
from utils import sortInput
from utils.rectangleFileLoader import load_rectangles_from_json
from visualizerImproved import VisualizerApp,AlgorithmVersion
from placement.RectangleSliding import rectangle_sliding
from placement.RectangleSlidingTesting import rectangle_sliding as rectangle_sliding_optimised


def build_container_from_solution(solution, rectangles, width):
    sorted_rects = sortInput.sort_with_keys(rectangles, solution)
    return rectangle_sliding(width, sorted_rects)

if __name__ == "__main__":
    width, rectangles = load_rectangles_from_json("problems/mid_256.json")

    directions = [random.random() for _ in rectangles]

    

    def on_gen_changed(ver_idx,gen_idx):
        #solution =
        if(ver_idx == 0):
            startt = time.perf_counter()
            container = rectangle_sliding_optimised(rectangles,directions)
            endt = time.perf_counter()
            print("optimised took: ",endt-startt)
            app.set_container(container)
        if(ver_idx == 1):
            startt = time.perf_counter()
            container = rectangle_sliding(rectangles,directions)
            endt = time.perf_counter()
            print("regular took: ",endt-startt)
            app.set_container(container)
        

    app = VisualizerApp(
        versions=[AlgorithmVersion("optimised",1),AlgorithmVersion("normal",1)],
        canvas_width=600,
        canvas_height=600,
    )

    app.on_generation_changed = on_gen_changed

    app.run()
