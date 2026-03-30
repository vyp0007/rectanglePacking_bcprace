import time
import pandas as pd

class ExperimentRunner:

    def __init__(self):
        self.results = []

    def run(self, algorithm_class, rectangles, containerWidth, config, dataset):
        start = time.time()

        algo = algorithm_class(rectangles, containerWidth, config)
        result = algo.run()

        runtime = time.time() - start

        self.results.append({
            "algorithm": dataset,
            "height": result["height"],
            "fitness": result["fitness"],
            "runtime": runtime,
            **config
        })

    def to_dataframe(self):
        return pd.DataFrame(self.results)
