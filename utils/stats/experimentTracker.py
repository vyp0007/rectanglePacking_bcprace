import time

class ExperimentTracker:
    def __init__(self):
        self.start_time = None
        self.records = []

    def start(self):
        self.start_time = time.perf_counter()

    def log(self, generation: int, best_score: float, best_height: float):
        elapsed = time.perf_counter() - self.start_time
        self.records.append({
            "generation": generation,
            "best_score": best_score,
            "best_height": best_height,
            "elapsed_time": elapsed
        })

    def get_dataframe(self):
        import pandas as pd
        return pd.DataFrame(self.records)

    def save_csv(self, path):
        self.get_dataframe().to_csv(path, index=False)
