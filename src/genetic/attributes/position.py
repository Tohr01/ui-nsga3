from typing import Optional
from numpy import random
from constants import CANVAS_WIDTH_NORM, CANVAS_HEIGHT_NORM
from genetic.mutation import normal_distribution_mutate
from genetic.recombination import intermediate_recombination
from genetic.reproducible import Reproducible


class Position(Reproducible):
    x: float
    y: float

    def __init__(
        self,
        x: Optional[float] = None,
        y: Optional[float] = None,
    ):
        self.x = x if x is not None else random.uniform(0, CANVAS_WIDTH_NORM)
        self.y = y if y is not None else random.uniform(0, CANVAS_HEIGHT_NORM)

    @staticmethod
    def crossover(i1: "Position", i2: "Position") -> "Position":
        """
        Crossover two Rectangles to produce a new Rectangle.
        We perform an intermediate recombination of x and y.
        :param i1: First Rectangle
        :param i2: Second Rectangle
        :return: New Rectangle
        """
        new_x = intermediate_recombination(i1.x, i2.x)
        new_y = intermediate_recombination(i1.y, i2.y)
        return Position(new_x, new_y)

    def mutate(self, mutation_rate: float):
        self.x = normal_distribution_mutate(
            value=self.x, mutation_rate=mutation_rate, i_max=CANVAS_WIDTH_NORM
        )
        self.y = normal_distribution_mutate(
            value=self.y, mutation_rate=mutation_rate, i_max=CANVAS_WIDTH_NORM
        )

    def mutatable_gene_count(self) -> int:
        return 2
