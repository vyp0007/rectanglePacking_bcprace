import random
import pandas as pd
from basicComponents.rectangle import Rectangle
from geneticAlgorithms.pygadGenetic import PygadGA
from tuning.experimentRunner import ExperimentRunner


# -----------------------------
# Problem Instance Creation
# -----------------------------

def generate_test_instance(n_rectangles=20, max_size=50):
    rectangles = []
    for _ in range(n_rectangles):
        w = random.randint(5, max_size)
        h = random.randint(5, max_size)
        rectangles.append(Rectangle(w, h))
    return rectangles


# -----------------------------
# Main
# -----------------------------

def main():

    random.seed(42)

    # Problem
    container_width = 200
    rectangles = generate_test_instance(n_rectangles=30)

    runner = ExperimentRunner()

    # Parameter ranges to test
    sol_per_pop_values = [20, 30, 40]
    num_generations_values = [20, 40, 60]

    runs_per_config = 5

    config_id = 0

    for sol_per_pop in sol_per_pop_values:
        for num_generations in num_generations_values:

            config_id += 1

            config = {
                "num_generations": num_generations,
                "sol_per_pop": sol_per_pop,
                "num_parents_mating": sol_per_pop // 2,
                "mutation_probability": 0.15,
            }

            for run_id in range(runs_per_config):
                print(f"\nRunning Config {config_id} | pop={sol_per_pop}, gen={num_generations}, Run {run_id + 1}")

                runner.run(
                    algorithm_class=PygadGA,
                    rectangles=rectangles,
                    containerWidth=container_width,
                    config=config,
                    label=f"pop_{sol_per_pop}_gen_{num_generations}"
                )

    # -----------------------------
    # Results
    # -----------------------------

    df = runner.to_dataframe()

    print("\n================ RAW RESULTS ================\n")
    print(df)

    print("\n================ SUMMARY ================\n")

    summary = df.groupby("algorithm").agg({
        "height": ["mean", "std", "min"],
        "runtime": ["mean"]
    })

    # Flatten multi-index columns
    summary.columns = ["_".join(col) for col in summary.columns]
    summary = summary.reset_index()

    # Time-efficiency metric (lower is better)
    summary["time_efficiency_score"] = (
        summary["height_mean"] * summary["runtime_mean"]
    )

    # Sort by best tradeoff
    summary = summary.sort_values("time_efficiency_score")

    print(summary)

    print("\n================ BEST CONFIG ================\n")
    print(summary.iloc[0])


if __name__ == "__main__":
    main()
