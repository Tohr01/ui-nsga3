from math import comb
from typing import Optional, cast

import numpy as np
from pymoo.algorithms.moo.unsga3 import UNSGA3
from pymoo.optimize import minimize
from pymoo.util.ref_dirs import get_reference_directions

from constants import (
    DEFAULT_FONT_FAMILY,
    MAX_OBJECTIVES_DAS_DENNIS,
)
from logger import get_new_logger
from optimization.nsga3.callback import ContainerCallback
from optimization.nsga3.crossover import ContainerCrossover
from optimization.nsga3.mutation import ContainerMutation
from optimization.nsga3.problem import ContainerProblem
from optimization.nsga3.repair import CanvasBoundsRepair
from optimization.nsga3.result import ContainerOptimizationResult, OptimizedContainer
from optimization.nsga3.sampling import ContainerSampling
from optimization.nsga3.select import select_best_container
from scoring.scorer import Scorer
from ui.blueprint import BlueprintContainer, RootBlueprint
from ui.canvas_context import CanvasContext
from ui.components.placeholder_container import PlaceholderContainer
from ui.element import TextlikeElement
from ui.text_measure import TextMeasure

logger = get_new_logger("optimization.nsga3.optimizer")


def _find_n_dd_partition(n_obj: int, target_points: int) -> int:
    """
    Find the number of partitions for Das-Dennis reference directions given the number of objectives and target points.
    Returns smallest p such that C(n_obj + p - 1, p) >= target_points
    The returned p will not always result in exactly target_points ref dirs!

    :param n_obj: The number of objectives
    :param target_points: The target number of reference directions to generate
    :return: Partition number for Das-Dennis reference directions
    """
    p = 1
    while comb(n_obj + p - 1, p) < target_points:
        p += 1

    # If p <= n_obj there is at most one interior point
    # Source: https://ieeexplore.ieee.org/abstract/document/9086772
    if p <= n_obj:
        logger.warning(
            f"The calculated number of partition {p = } for {n_obj = } objectives is less than or equal to the number of objectives."
        )

    return p


def _get_ref_dirs_and_pop_size(
    n_obj: int, min_pop_size: int, seed: Optional[int]
) -> tuple[np.ndarray, int]:
    """
    Get reference directions for NSGA-III optimization.
    The target number of directions is calculated as 64 * n_obj
    For 1 objective ref dirs not used and pop size is set to max(min_pop_size, target_points)
    For 2-MAX_OBJECTIVES_DAS_DENNIS objectives use Das-Dennis reference directions with the number of partitions calculated to be close to target_points
    For more than 4 objectives use Riesz s-energy reference directions with the number of points set to target_points

    :param n_obj: The number of objectives
    :param min_pop_size: The minimum population size
    :param seed: The random seed to use for reference direction generation (for energy-based reference
    :return: A tuple of (reference directions, population size [multiple of 4])
    """
    target_points = max(min_pop_size, 64 * n_obj)

    def _round_to_multiple_of_4(x: int) -> int:
        return x if x % 4 == 0 else x + (4 - x % 4)

    # For 1 objective ref dirs not used
    if n_obj == 1:
        return np.array([[1.0]]), _round_to_multiple_of_4(target_points)

    if n_obj <= MAX_OBJECTIVES_DAS_DENNIS:
        # Use das-dennis for reference dirs
        p = _find_n_dd_partition(n_obj, target_points)
        ref_dirs = get_reference_directions("das-dennis", n_dim=n_obj, n_partitions=p)
    else:
        # Use Riesz s-energy for reference dirs
        ref_dirs = get_reference_directions(
            "energy", n_dim=n_obj, n_points=target_points, seed=seed
        )

    return ref_dirs, _round_to_multiple_of_4(len(ref_dirs))


def run_nsga3_optimization(
    root_blueprint: RootBlueprint,
    n_gen: int,
    min_pop_size: int,
    seed: Optional[int],
    constraints: list[Scorer] = [],
    mutation_rate: float = 0.1,
    collect_metrics: bool = False,
) -> dict[str, ContainerOptimizationResult]:
    """
    Runs the NSGA-III optimization algorithm on the given root blueprint.
    The pymoo minimize function will use the optionally provided seed.
    Note however that other randomly dependent components of the optimization
    (like sampling, mutation, etc.) should also be initialized with the same seed to ensure
    reproducibility before calling this function.

    :param root_blueprint: The root blueprint to optimize
    :param n_gen: The number of generations to run optimization for
    :param min_pop_size: The minimum population size (will be used for reference direction generation)
    :param seed: The random seed to use for optimization (pymoo minimize function)
    :param constraints: A list of constraint scorers to apply during optimization (ieq constraints)
    :param mutation_rate: The mutation rate to use for the ContainerMutation operator
    :param collect_metrics: Whether to record optimization results to disk (included in ContainerOptimizationResult)

    :return: A dictionary of blueprint_id to optimized Container
    """

    # Queue of triples of (container_width_px, container_height_px, blueprint)
    queue: list[tuple[float, float, BlueprintContainer]] = [
        (root_blueprint.width_px, root_blueprint.height_px, root_blueprint)
    ]
    optimized_containers: dict[str, ContainerOptimizationResult] = {}

    while queue:
        width_px, height_px, current_blueprint = queue.pop(0)
        logger.info(
            f"Optimizing blueprint {current_blueprint.label} with size ({width_px}px, {height_px}px)"
        )

        # Set canvas dimensions
        CanvasContext.get_instance().set_canvas_dim(width_px, height_px)

        # Init genetic components for NSGA-III
        bounds_repair = CanvasBoundsRepair()
        sampling = ContainerSampling(
            width_px, height_px, current_blueprint, bounds_repair
        )
        crossover = ContainerCrossover()
        mutation = ContainerMutation(mutation_rate=mutation_rate)
        problem = ContainerProblem(current_blueprint.get_scorers(), constraints)

        # We try to optimize an empty container
        # Store random container as the best container for the current blueprint
        if len(current_blueprint.elements) == 0:
            best_container = OptimizedContainer(
                container=sampling.get_single_container(), summed_score=0.0
            )
            empty_container_optimization_result = ContainerOptimizationResult(
                blueprint=current_blueprint,
                pop_size=0,
                ref_dir_count=0,
                best_container=best_container,
                optimized_by_algorithm=False,
            )
            optimized_containers[current_blueprint.blueprint_id] = (
                empty_container_optimization_result
            )
            logger.info(
                f"Blueprint {current_blueprint.label} has no elements, storing random container as best"
            )
            continue

        # Cache text measurement for all text elements
        text_measure = TextMeasure.get_instance()
        for element_type, element_args in current_blueprint.flattend_elements:
            if issubclass(element_type, TextlikeElement):
                text_measure.precache_font_sizes(
                    text=element_args["text"],
                    font_family=element_args.get("font_family", DEFAULT_FONT_FAMILY),
                )

        ref_dirs, pop_size = _get_ref_dirs_and_pop_size(
            n_obj=len(current_blueprint.scorers), min_pop_size=min_pop_size, seed=seed
        )
        logger.info(
            f"Amount of reference directions: {len(ref_dirs)}; Population size: {pop_size}"
        )

        container_optimization_result = ContainerOptimizationResult(
            blueprint=current_blueprint, pop_size=pop_size, ref_dir_count=len(ref_dirs)
        )

        callback = ContainerCallback(
            n_gen, container_optimization_result, collect_metrics
        )
        algorithm = UNSGA3(
            pop_size=pop_size,
            ref_dirs=ref_dirs,
            sampling=sampling,  # type: ignore
            crossover=crossover,  # type: ignore
            mutation=mutation,  # type: ignore
            repair=bounds_repair,
            callback=callback,
            eliminate_duplicates=False,
        )

        result = minimize(
            problem=problem,
            algorithm=algorithm,
            termination=("n_gen", n_gen),
            seed=seed,
            verbose=False,
        )

        # Store result in optimization result
        container_optimization_result.result = result

        # Extract results from algorithm because pymoo deepcopies callback + algorithm meaning our original
        # reference to the optimization result is not updated
        algorithm = cast(UNSGA3, result.algorithm)
        callback = cast(ContainerCallback, algorithm.callback)
        container_optimization_result = callback.optimization_result

        # Type validation for results
        if not (
            isinstance(result.X, np.ndarray)
            and isinstance(result.F, np.ndarray)
            and isinstance(result.CV, np.ndarray)
        ):
            raise RuntimeError(
                f"Optimization did not return any solutions for container {current_blueprint.label}"
            )

        # Pick a solution
        best_F, best_container = select_best_container(
            current_blueprint, result.F, result.CV, result.X
        )

        # Map the container id to the size of the child container
        container_sizes = {}
        for e in best_container.elements:
            if isinstance(e, PlaceholderContainer):
                container_width_px = e.size.width * best_container.width_px
                container_height_px = e.size.height * best_container.height_px
                container_sizes[e.blueprint_id] = (
                    container_width_px,
                    container_height_px,
                )

        children_blueprints = []
        for element in current_blueprint.elements:
            if isinstance(element, BlueprintContainer):
                blueprint_id = element.blueprint_id
                # Get the size of the child container by container id
                width_px, height_px = container_sizes[blueprint_id]

                children_blueprints.append((width_px, height_px, element))

        queue.extend(children_blueprints)

        # Store best container and optimization result for the current blueprint
        best_optimized_container = OptimizedContainer(
            container=best_container, summed_score=best_F.sum()
        )
        container_optimization_result.best_container = best_optimized_container
        container_optimization_result.execution_time_sec = cast(float, result.exec_time)

        optimized_containers[current_blueprint.blueprint_id] = (
            container_optimization_result
        )

        # Clear text measurement cache
        logger.info("Clearing text measurement cache...")
        text_measure.clear_cache()

    TextMeasure.get_instance().close()

    return optimized_containers
