import random
from pathlib import Path

import numpy as np
from pymoo.algorithms.moo.nsga3 import NSGA3
from pymoo.optimize import minimize
from pymoo.util.ref_dirs import get_reference_directions

from optimization.nsga3.crossover import ContainerCrossover
from optimization.nsga3.mutation import ContainerMutation
from optimization.nsga3.problem import ContainerProblem
from optimization.nsga3.repair import CanvasBoundsRepair
from optimization.nsga3.sampling import ContainerSampling
from ui.renderer import HTMLRenderer
from ui.structure import (
    BlueprintContainer,
    interface_blueprint,
)

SEED = 42

random.seed(SEED)
np.random.seed(SEED)

optimization_queue: list[tuple[float, float, BlueprintContainer]] = [
    (interface_blueprint.width_px, interface_blueprint.height_px, interface_blueprint)
]


while optimization_queue:
    width_px, height_px, current_blueprint = optimization_queue.pop(0)

    # Init genetic components for NSGA-III
    sampling = ContainerSampling(width_px, height_px, current_blueprint)
    crossover = ContainerCrossover()
    mutation = ContainerMutation(mutation_rate=0.1)
    problem = ContainerProblem(current_blueprint.scorers)
    bounds_repair = CanvasBoundsRepair()

    ref_dirs = get_reference_directions(
        "das-dennis", n_dim=problem.n_obj, n_partitions=20, seed=SEED
    )
    algorithm = NSGA3(
        ref_dirs=ref_dirs,
        sampling=sampling,
        crossover=crossover,
        mutation=mutation,
        repair=bounds_repair,
        eliminate_duplicates=False,
    )

    results = minimize(
        problem=problem,
        algorithm=algorithm,
        termination=("n_gen", 200),
        seed=SEED,
        verbose=False,
    )

    # Select the best container based on the following criteria:
    # 1. Containers with lowest constraint violation
    # 2. Among those pick container with best objective values (summing all objectives; minimize)
    containers = results.X[:, 0]
    objective_values = results.F
    aggr_constraint_violations: np.ndarray = results.CV.flatten()
    min_constraint_violation_idxs = np.where(
        aggr_constraint_violations == np.min(aggr_constraint_violations)
    )[0]

    summed_objective_values = np.sum(objective_values, axis=1)
    assert len(summed_objective_values) == len(aggr_constraint_violations), (
        "Length of summed objective values and aggregated constraint violations must be the same."
    )
    best_container_idx = min_constraint_violation_idxs[
        np.argmin(summed_objective_values[min_constraint_violation_idxs])
    ]

    # TODO: Store container
    best_container = containers[best_container_idx]
    HTMLRenderer.write_container_to_html(
        best_container, Path(f"best_container_{id(best_container)}.html")
    )

    # TODO: adds new blueprints to optimization queue

    break
