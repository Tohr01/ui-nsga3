from typing import Optional

from numpy import random

from genetic.mutation import normal_distribution_mutate
from genetic.recombination import intermediate_recombination
from genetic.reproducible import Reproducible


class Size(Reproducible):
    """
    Size class gene representing dimensions in 2D normalized space usually width, height ∈ [0; 1]
    A lower bound of 0 is enforced to disallow negative sizes.
    """

    width: float
    height: float

    def __init__(self, width: Optional[float] = None, height: Optional[float] = None):
        """
        Initialize a new Size object with optional width and height.
        :param width: Optional width (if not set pick from uniform(0, 1))
        :param height: Optional height (if not set pick from uniform(0, 1))
        NOTE: Will clamp width and height to be >= 0 to disallow negative sizes.
        """
        self.width, self.height = (self._init_dimension(d) for d in (width, height))

    def _init_dimension(self, dimension: Optional[float]) -> float:
        return max(dimension, 0) if dimension is not None else random.uniform(0, 1)

    @staticmethod
    def crossover(i1: "Size", i2: "Size") -> "Size":
        """
        Crossover two Sizes to produce a new Size.
        We perform an intermediate recombination of width and height.
        Clamp size to be >= 0 to disallow negative sizes.

        :param i1: First Size
        :param i2: Second Size
        :return: New Size
        """
        new_width = intermediate_recombination(i1.width, i2.width)
        new_height = intermediate_recombination(i1.height, i2.height)

        new_height = max(0, new_height)
        new_width = max(0, new_width)
        return Size(new_width, new_height)

    def mutate(self, mutation_rate: float):
        """
        Mutate the Size by applying a normal distribution mutation to width and height.
        Clamp size to be >= 0 to disallow negative sizes.
        :param mutation_rate: The probability of mutation for each dimension.
        """
        self.width = max(
            0,
            normal_distribution_mutate(value=self.width, mutation_rate=mutation_rate),
        )
        self.height = max(
            0,
            normal_distribution_mutate(value=self.height, mutation_rate=mutation_rate),
        )

    @property
    def area(self) -> float:
        """
        Calculates the area of the size.
        :return: Area (width * height)
        """
        return self.width * self.height

    def get_wh(self) -> tuple[float, float]:
        """
        Returns the width and height of the Size as a tuple.
        :return: Tuple of (width, height)
        """
        return self.width, self.height
