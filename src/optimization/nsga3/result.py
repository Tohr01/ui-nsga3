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
    # F: 2D np.array; G: 2D np.array;
    # CV: 1D np.array; best_container: OptimizedContainer
    df: pd.DataFrame = field(
        default_factory=lambda: pd.DataFrame(
            columns=["generation", "F", "G", "CV", "best_container"]
        )
    )


def print_result_overview(optimization_results: dict[str, ContainerOptimizationResult]):
    aggr_ui_score = sum(
        optimization_result.best_container.summed_score
        for optimization_result in optimization_results.values()
        if optimization_result.best_container is not None
    )
    label_score_dict = {
        optimization_result.blueprint.label: optimization_result.best_container.summed_score
        for optimization_result in optimization_results.values()
        if optimization_result.best_container is not None
    }
    if not label_score_dict:
        raise ValueError("No best containers found in optimization results.")

    w = max(len(label) for label in label_score_dict.keys()) + 2

    print()
    for label, score in label_score_dict.items():
        print(f"{label:<{w}}{score}")

    print(f"\nAggregated UI score: {aggr_ui_score}")
    print()
