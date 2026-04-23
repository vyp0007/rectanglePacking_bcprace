from placement.otherAlgorithms.bottomLeftFill import bottom_left_fill
from utils import sortInput
from utils.rectangleFileLoader import load_rectangles_from_json
from visualizer import VisualizerApp
from placement import bottomLeftFillSortedLists


def build_container_from_solution(solution, rectangles, width):
    sorted_rects = sortInput.sort_with_keys(rectangles, solution)
    return bottom_left_fill(width, sorted_rects)

if __name__ == "__main__":
    width, rectangles = load_rectangles_from_json("problems/large_600.json")

    app = VisualizerApp(
        num_generations=1,
        num_populations=1,
        container_width=width,
        canvas_width=600,
        canvas_height=600,
    )

    def on_gen_changed(gen_idx):
        #solution = 
        container = bottomLeftFillSortedLists.bottom_left_fill(width,rectangles)
        app.set_container(container)

    def on_pop_changed(gen_idx, pop_idx):
        container = bottomLeftFillSortedLists.bottom_left_fill(width,rectangles)
        app.set_container(container)

    app.on_generation_changed = on_gen_changed
    app.on_population_changed = on_pop_changed

    # load initial view
    on_gen_changed(0)

    app.run()
