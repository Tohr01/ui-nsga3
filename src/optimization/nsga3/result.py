from dataclasses import dataclass, field
from typing import Optional

import pandas as pd

from ui.blueprint import BlueprintContainer
from ui.container import Container


@dataclass
class OptimizedContainer:
    container: Container
    summed_score: float


@dataclass
class ContainerOptimizationResult:
    blueprint: BlueprintContainer
    pop_size: int
    ref_dir_count: int
    best_container: Optional[OptimizedContainer] = None
    execution_time_sec: float = 0.0
    optimized_by_algorithm: bool = True
    df: pd.DataFrame = field(
        default_factory=lambda: pd.DataFrame(columns=["generation", "F", "G", "CV"])
    )
