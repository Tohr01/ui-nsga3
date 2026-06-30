from optimization.nsga3.result import ContainerOptimizationResult
from ui.container import Container


def container_optimization_results_to_optimized_containers(
    optimized_container_results: dict[str, ContainerOptimizationResult],
) -> dict[str, Container]:
    """
    Convert a dictionary of ContainerOptimizationResult to a dictionary of optimized Containers
    such that the key is the original blueprint_id (like in the input) and the value is the optimized
    Container.

    :param optimized_container_results: Dictionary of ContainerOptimizationResult
    :return: Dictionary of optimized Containers
    """
    optimized_containers: dict[str, Container] = {}
    for blueprint_id, optimization_result in optimized_container_results.items():
        if optimization_result.best_container is None:
            raise ValueError(
                f"Optimization result for blueprint_id {blueprint_id} has no best container."
            )
        optimized_containers[blueprint_id] = (
            optimization_result.best_container.container
        )
    return optimized_containers
