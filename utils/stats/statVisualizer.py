import pandas as pd
import matplotlib.pyplot as plt


class ExperimentVisualizer:

    @staticmethod
    def plot_from_csv(path):
        df = pd.read_csv(path)

        fig, ax1 = plt.subplots()

        # ---- Primary axis (Height) ----
        color1 = "tab:blue"
        ax1.set_xlabel("Generation")
        ax1.set_ylabel("Height", color=color1)
        ax1.plot(df["generation"], df["best_height"], color=color1)
        ax1.tick_params(axis="y", labelcolor=color1)

        # ---- Secondary axis (Time) ----
        ax2 = ax1.twinx()
        color2 = "tab:red"
        ax2.set_ylabel("Elapsed Time (s)", color=color2)
        ax2.plot(df["generation"], df["elapsed_time"], color=color2)
        ax2.tick_params(axis="y", labelcolor=color2)

        plt.title("Algorithm Performance Over Generations")
        plt.tight_layout()
        plt.show()