from typing import Optional

from numpy import random

from genetic.mutation import normal_distribution_mutate
from genetic.recombination import intermediate_recombination
from genetic.reproducible import Reproducible


class Position(Reproducible):
    """
    Position class gene representing a point in 2D normalized space usually x, y ∈ [0; 1]
    A lower or upper bound are not enforced.
    """

    x: float
    y: float

    def __init__(
        self,
        x: Optional[float] = None,
        y: Optional[float] = None,
    ):
        """
        Initialize a new Position object with optional x and y coordinates.

        :param x: Optional x coordinate (if not set pick from uniform(0, 1))
        :param y: Optional y coordinate (if not set pick from uniform(0, 1))
        """
        self.x, self.y = (self._init_dimension(d) for d in (x, y))

    def _init_dimension(self, dimension: Optional[float]) -> float:
        return dimension if dimension is not None else random.uniform(0, 1)

    @staticmethod
    def crossover(i1: "Position", i2: "Position") -> "Position":
        """
        Crossover two Positions to produce a new Position.
        We perform an intermediate recombination of x and y.

        :param i1: First Position
        :param i2: Second Position
        :return: New Position
        """
        new_x = intermediate_recombination(i1.x, i2.x)
        new_y = intermediate_recombination(i1.y, i2.y)
        return Position(new_x, new_y)

    def mutate(self, mutation_rate: float):
        """
        Mutate the Position by applying a normal distribution mutation to x and y.
        :param mutation_rate: The probability of mutation for each coordinate.
        """
        self.x = normal_distribution_mutate(value=self.x, mutation_rate=mutation_rate)
        self.y = normal_distribution_mutate(value=self.y, mutation_rate=mutation_rate)

    def get_xy(self) -> tuple[float, float]:
        """
        Returns the x and y coordinates of the Position as a tuple.
        :return: Tuple of (x, y)
        """
        return self.x, self.y
