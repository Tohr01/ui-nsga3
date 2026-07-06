from typing import Optional

import pandas as pd
from pymoo.algorithms.moo.unsga3 import UNSGA3
from pymoo.core.callback import Callback
from tqdm import tqdm

from optimization.nsga3.result import ContainerOptimizationResult, OptimizedContainer
from optimization.nsga3.select import select_best_container


class ContainerCallback(Callback):
    """
    Custom callback class for NSGA3 optimization algorithm to track the optimization
    progress and store the results in a ContainerOptimizationResult object.
    Also displays a progress bar indicating the number of generations completed out of n_gen.
    """

    optimization_result: ContainerOptimizationResult
    n_gen: int
    collect_metrics: bool
    pbar: Optional[tqdm]

    def __init__(
        self,
        n_gen: int,
        optimization_result: ContainerOptimizationResult,
        collect_metrics: bool = True,
    ):
        """
        Initialize the ContainerCallback with the total number of generations and the optimization result object.
        :param n_gen: Total number of generations for the optimization algorithm.
        :param optimization_result: ContainerOptimizationResult object to store the optimization results.
        :param collect_metrics: Whether to collect metrics during the optimization process.
        """
        self.optimization_result = optimization_result
        self.n_gen = n_gen
        self.collect_metrics = collect_metrics
        self.pbar = None
        super().__init__()

    def notify(self, algorithm: UNSGA3):
        # Update progress bar
        if self.pbar is None:
            self.pbar = tqdm(total=self.n_gen, desc="Generations", unit="gen")
        self.pbar.update(1)

        if not algorithm.has_next():
            self.pbar.close()

        if not self.collect_metrics:
            return

        if algorithm.pop is None:
            raise ValueError("Algorithm population is None. This should not happen.")

        F = algorithm.pop.get("F")  # Objective values
        G = algorithm.pop.get("G")  # Constraint violation vectors
        CV = algorithm.pop.get("CV").flatten()  # Aggregated constraint violation
        X = algorithm.pop.get("X").flatten()  # Containers
        best_F, best_container = select_best_container(
            self.optimization_result.blueprint, F, CV, X, supress_logger=True
        )

        data = {
            "generation": algorithm.n_gen,
            "F": F,
            "G": G,
            "CV": CV,
            "best_container": OptimizedContainer(
                best_container, best_F.sum()
            ),  # wrt all objectives & weights
        }

        # Append to the optimization result df
        self.optimization_result.df = pd.concat(
            [self.optimization_result.df, pd.DataFrame([data])], ignore_index=True
        )
