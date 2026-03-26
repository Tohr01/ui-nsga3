import numpy as np
from pymoo.core.crossover import Crossover

from ui.container import Container


class ContainerCrossover(Crossover):
    def __init__(self):
        super().__init__(n_parents=2, n_offsprings=1)

    def _do(self, problem, X, *args, random_state=None, **kwargs):
        _, n_matings, _ = X.shape
        offspring = np.empty((1, n_matings, 1), dtype=Container)
        for i in range(n_matings):
            p1 = X[0, i, 0]
            p2 = X[1, i, 0]
            child = type(p1).crossover(p1, p2)
            offspring[0, i, 0] = child

        return offspring
