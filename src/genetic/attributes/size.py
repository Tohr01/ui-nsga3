from typing import Optional
from genetic.mutation import normal_distribution_mutate
from genetic.recombination import intermediate_recombination
from genetic.reproducible import Reproducible
from numpy import random


class Size(Reproducible):
    width: float
    height: float

    def __init__(self, width: Optional[float] = None, height: Optional[float] = None):
        self.width, self.height = (self._init_dimension(dim) for dim in (width, height))

    def _init_dimension(self, value: Optional[float]) -> float:
        assert value is None or 0 <= value, "Size dimensions must be non-negative"
        return value if value is not None else random.uniform(0, 1)

    @staticmethod
    def crossover(i1: "Size", i2: "Size") -> "Size":
        new_width = intermediate_recombination(i1.width, i2.width)
        new_height = intermediate_recombination(i1.height, i2.height)

        new_height = max(0, new_height)
        new_width = max(0, new_width)
        return Size(new_width, new_height)

    def mutate(self, mutation_rate: float):
        self.width = max(
            0, normal_distribution_mutate(value=self.width, mutation_rate=mutation_rate)
        )
        self.height = max(
            0,
            normal_distribution_mutate(value=self.height, mutation_rate=mutation_rate),
        )

    def mutatable_gene_count(self) -> int:
        return 2

    def area(self) -> float:
        """
        Calculates the area of the size.
        """
        return self.width * self.height
