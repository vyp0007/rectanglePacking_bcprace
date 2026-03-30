from dataclasses import dataclass

@dataclass
class GenerationStats:
    generation: int
    best_score: float
    best_height: float
    elapsed_time: float
