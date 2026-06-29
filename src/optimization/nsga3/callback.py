from typing import Optional

import pandas as pd
from pymoo.algorithms.moo.unsga3 import UNSGA3
from pymoo.core.callback import Callback
from tqdm import tqdm

from optimization.nsga3.result import ContainerOptimizationResult


class ContainerCallback(Callback):
    optimization_result: ContainerOptimizationResult
    n_gen: int
    pbar: Optional[tqdm]

    def __init__(
        self, n_gen: int, optimization_result: ContainerOptimizationResult
    ) -> None:
        self.optimization_result = optimization_result
        self.n_gen = n_gen
        self.pbar = None
        super().__init__()

    def notify(self, algorithm: UNSGA3):
        # Update progress bar
        if self.pbar is None:
            self.pbar = tqdm(total=self.n_gen, desc="Generations", unit="gen")
        self.pbar.update(1)

        if algorithm.pop is None:
            raise ValueError("Algorithm population is None. This should not happen.")

        data = {
            "generation": algorithm.n_gen,
            "F": algorithm.pop.get("F"),  # Objective values
            "G": algorithm.pop.get("G"),  # Constraint violation
            "CV": algorithm.pop.get("CV"),  # Aggregated constraint violation
        }
        # Hypervolume indicator
        # H. Ishibuchi, R. Imada, Y. Setoguchi, and Y. Nojima,
        # “How to specify a reference point in hypervolume calculation for fair performance comparison,”
        # Evolutionary Computation, vol. 26, no. 3, pp. 411–440, May 2018, doi: 10.1162/evco_a_00226.
        # -> We select a ref point that is 10% bigger then the nadir point; Comparability between different containers
        # hv_ref_vector = np.ones(F.shape[1]) * 1.1
        # hv = Hypervolume(ref_point=hv_ref_vector)
        # data["HV"] = hv.do(F)

        # Append to the optimization result df
        self.optimization_result.df = pd.concat(
            [self.optimization_result.df, pd.DataFrame([data])], ignore_index=True
        )
        # self.optimization_result.df.loc[len(self.optimization_result.df)] = data

        if not algorithm.has_next():
            self.pbar.close()
