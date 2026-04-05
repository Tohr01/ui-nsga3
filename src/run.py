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
from ui.components.placeholder_container import PlaceholderContainer
from ui.container import Container
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

optimized_containers: dict[str, Container] = {}


while optimization_queue:
    width_px, height_px, current_blueprint = optimization_queue.pop(0)

    # Init genetic components for NSGA-III
    sampling = ContainerSampling(width_px, height_px, current_blueprint)
    crossover = ContainerCrossover()
    mutation = ContainerMutation(mutation_rate=0.1)
    problem = ContainerProblem(current_blueprint.scorers)
    bounds_repair = CanvasBoundsRepair()

    # We try to optimize an empty container
    # Store random container as the best container for the current blueprint
    if len(current_blueprint.elements) == 0:
        best_container = sampling.get_single_container()
        optimized_containers[best_container.blueprint_id] = best_container
        HTMLRenderer.write_container_to_html(
            best_container, Path(f"best_container_{best_container.blueprint_id}.html")
        )
        continue

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
    # TODO: Handle X empty. Can this occur?
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
    best_container: Container = containers[best_container_idx]
    optimized_containers[best_container.blueprint_id] = best_container

    HTMLRenderer.write_container_to_html(
        best_container, Path(f"best_container_{best_container.blueprint_id}.html")
    )

    # Map the container id to the size of the child container
    container_sizes = {}
    for e in best_container.elements:
        if isinstance(e, PlaceholderContainer):
            container_width_px = e.size.width * best_container.width_px
            container_height_px = e.size.height * best_container.height_px
            container_sizes[e.blueprint_id] = (container_width_px, container_height_px)

    children_blueprints = []
    for element in current_blueprint.elements:
        if isinstance(element, BlueprintContainer):
            blueprint_id = element.blueprint_id
            # Get the size of the child container by container id
            assert blueprint_id in container_sizes, (
                f"Blueprint with id {blueprint_id} not found in container sizes."
            )
            width_px, height_px = container_sizes[blueprint_id]

            children_blueprints.append((width_px, height_px, element))

    optimization_queue.extend(children_blueprints)
print(optimized_containers)


def assemble_containers(
    root_container: Container, containers: dict[str, Container]
) -> Container:
    pass
