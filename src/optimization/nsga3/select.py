import numpy as np
from pymoo.decomposition.weighted_sum import WeightedSum

from logger import get_new_logger
from ui.blueprint import BlueprintContainer
from ui.container import Container

logger = get_new_logger("optimizer.nsga3.select")


# TODO: Make this work for one objective
def select_best_container(
    blueprint: BlueprintContainer,
    F: np.ndarray,
    CV: np.ndarray,
    X: np.ndarray,
    supress_logger: bool = False,
) -> tuple[np.ndarray, Container]:
    """
    Select the best container based on objective function values, aggregated function violation,
    and the corresponding containers.
    1. Find feasible solutions (CV <= 0)
    2. If feasible solutions exist, choose the one with min weighted sum of objectives
    3. If no feasible solutions exist, choose the one with min constraint violation

    :param blueprint: BlueprintContainer object used for optimization
    :param F: Objective function values
    :param CV: Constraint violation values
    :param X: Containers
    :param supress_logger: If True, logger will be suppressed (useful for use in e.g. callback)
    :return: Tuple containing the best objective function values and the corresponding container
    """
    feasible_mask = CV[:, 0] <= 0.0
    if feasible_mask.any():
        feasible_F = F[feasible_mask]
        feasible_X = X[feasible_mask]
        weights = blueprint.get_normalized_scorer_weight_arr()

        decomb = WeightedSum()
        best_feasible_idx = decomb.do(feasible_F, weights).argmin()
        best_F = feasible_F[best_feasible_idx]
        best_container = feasible_X[best_feasible_idx, 0]
    else:
        if not supress_logger:
            logger.warning(
                "No feasible solutions found, picking best among all solutions with lowest constraint violation"
            )
        best_container_idx = CV[:, 0].argmin()
        best_F = F[best_container_idx]
        best_container = X[best_container_idx, 0]

    return best_F, best_container
