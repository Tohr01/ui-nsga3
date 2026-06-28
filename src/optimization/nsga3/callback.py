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

        data = {}
        data["generation"] = algorithm.n_gen
        if algorithm.pop is None:
            raise ValueError("Algorithm population is None. This should not happen.")

        # Objective values
        F = algorithm.pop.get("F")
        data["F"] = F

        # Contraint values
        G = algorithm.pop.get("G")
        data["G"] = G

        # Aggregated constraint violations
        CV = algorithm.pop.get("CV")
        data["CV"] = CV

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

    def close(self):
        if self.pbar is not None:
            self.pbar.close()
