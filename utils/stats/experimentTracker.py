import time

class ExperimentTracker:
    def __init__(self, name = None):
        self.start_time = None
        self.name = name
        self.records = []
        self._best_so_far = {
            "best_score": None,
            "best_height": None,
            "best_width": None,
            "best_density": None
        }

    def _update_best(self, best_score, best_height, best_width, best_density):
        if best_score is None:
            return

        current_best = self._best_so_far["best_score"]

        if current_best is None or best_score > current_best:
            self._best_so_far = {
                "best_score": best_score,
                "best_height": best_height,
                "best_width": best_width,
                "best_density": best_density
            }

    def start(self):
        self.start_time = time.perf_counter()

    def log(
        self,
        generation: int,
        best_score: float = None,
        best_height: float = None,
        best_width: float = None,
        best_density: float = None
    ):
        elapsed = time.perf_counter() - self.start_time

        self._update_best(best_score, best_height, best_width, best_density)

        self.records.append({
            "generation": generation,
            "best_score": self._best_so_far["best_score"],
            "best_height": self._best_so_far["best_height"],
            "best_width": self._best_so_far["best_width"],
            "best_density": self._best_so_far["best_density"],
            "elapsed_time": elapsed
        })

    def add_stats(
        self,
        generation: int,
        best_score: float = None,
        best_height: float = None,
        best_width: float = None,
        best_density: float = None
    ):
        self._update_best(best_score, best_height, best_width, best_density)

        for record in self.records:
            if record["generation"] == generation:
                # overwrite with BEST SO FAR
                record["best_score"] = self._best_so_far["best_score"]
                record["best_height"] = self._best_so_far["best_height"]
                record["best_width"] = self._best_so_far["best_width"]
                record["best_density"] = self._best_so_far["best_density"]
                return

        raise ValueError(f"Generation {generation} not found")

    def get_dataframe(self):
        import pandas as pd
        return pd.DataFrame(self.records)

    def save_csv(self, path):
        self.get_dataframe().to_csv(path, index=False)

    def save_latex(
        self,
        path,
        columns=None,
        float_format="%.4f",
        caption=None,
        label=None
    ):
        """
        Export the tracked results into a LaTeX table.

        :param path: Output .tex file path
        :param columns: Optional list of columns to include/order
        :param float_format: Formatting for floats
        :param caption: Optional LaTeX table caption
        :param label: Optional LaTeX label for referencing
        """
        df = self.get_dataframe()

        if columns is not None:
            df = df[columns]

        latex_str = df.to_latex(
            index=False,
            float_format=float_format,
            caption=caption,
            label=label,
            longtable=False
        )

        with open(path, "w") as f:
            f.write(latex_str)