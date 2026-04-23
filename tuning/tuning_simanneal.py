import random
import pandas as pd
from itertools import product

from geneticAlgorithms.simannealSA import SimulatedAnnealing
from tuning.experimentRunner import ExperimentRunner
from basicComponents.rectangle import Rectangle
from utils.rectangleFileLoader import load_rectangles_from_json


def generate_dataset(n, container_width):
    """
    Simple rectangle generator for experiments.
    Replace this with your own dataset loader if needed.
    """

    rects = []

    for _ in range(n):
        w = random.randint(1, container_width // 4)
        h = random.randint(1, container_width // 4)
        rects.append(Rectangle(w, h))

    return rects


def build_datasets():
    """
    Create datasets of different sizes.
    """

    small = load_rectangles_from_json("problems/small_125.json")
    mid = load_rectangles_from_json("problems/mid_256.json")


    datasets = [
        ("small_125", small[1], small[0]),
        #("medium_256", mid[1], mid[0])
    ]

    return datasets


def build_param_grid():
    """
    Hyperparameter grid for simulated annealing.
    """

    param_grid = {
        "Tmax": [100, 500, 800],
        "Tmin": [1,0.1, 0.001],
        "steps": [3000]
    }

    configs = [
        dict(zip(param_grid.keys(), values))
        for values in product(*param_grid.values())
    ]

    return configs


def run_experiments():

    datasets = build_datasets()
    param_configs = build_param_grid()

    repeats = 3

    runner = ExperimentRunner()

    total_runs = len(datasets) * len(param_configs) * repeats
    run_counter = 0

    for dataset_name, rectangles, containerWidth in datasets:

        for config in param_configs:

            for run in range(repeats):

                run_counter += 1
                print(f"Run {run_counter}/{total_runs} | Dataset={dataset_name} | Config={config} | Repeat={run}")

                random.seed(run)

                runner.run(
                    SimulatedAnnealing,
                    rectangles,
                    containerWidth,
                    config,
                    dataset=dataset_name
                )

    return runner


def analyze_results(runner):

    df = runner.to_dataframe()
    df = df.sort_values(by="fitness", ascending=False)

    print("\nRaw results:")
    print(df.head())

    summary = (
        df.groupby(["algorithm", "Tmax", "Tmin", "steps"])
        .agg({
            "height": ["mean", "std", "min"],
            "runtime": "mean"
        })
        .reset_index()
    )

    print("\nSummary statistics:")
    print(summary)

    df.to_csv("sa_results_raw.csv", index=False)
    summary.to_csv("sa_results_summary.csv", index=False)

    print("\nResults saved:")
    print("sa_results_raw.csv")
    print("sa_results_summary.csv")


def main():

    runner = run_experiments()

    analyze_results(runner)


if __name__ == "__main__":
    main()