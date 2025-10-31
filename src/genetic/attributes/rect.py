import numpy.random as random
from genetic.mutation import normal_distribution_mutate
from genetic.recombination import intermediate_recombination
from genetic.reproducible import Reproducible


class Rect(Reproducible):
    x: float
    y: float
    width: float
    height: float

    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @staticmethod
    def random() -> "Rect":
        return Rect(
            x=random.random(),
            y=random.random(),
            width=random.random(),
            height=random.random(),
        )

    @staticmethod
    def crossover(i1: "Rect", i2: "Rect") -> "Rect":
        """
        Crossover two Rectangles to produce a new Rectangle.
        We perform an intermediate recombination of x, y, width and height.
        :param i1: First Rectangle
        :param i2: Second Rectangle
        :return: New Rectangle
        """
        new_x = intermediate_recombination(i1.x, i2.x)
        new_y = intermediate_recombination(i1.y, i2.y)
        # We ensure that width and height are non-negative
        new_width = max(0, intermediate_recombination(i1.width, i2.width))
        new_height = max(0, intermediate_recombination(i1.height, i2.height))
        return Rect(new_x, new_y, new_width, new_height)

    def mutate(self, mutation_rate: float):
        mutation_rate /= 4
        self.x = normal_distribution_mutate(value=self.x, mutation_rate=mutation_rate)
        self.y = normal_distribution_mutate(value=self.y, mutation_rate=mutation_rate)
        # We ensure that width and height are non-negative
        self.width = max(
            0,
            normal_distribution_mutate(value=self.width, mutation_rate=mutation_rate),
        )
        self.height = max(
            0,
            normal_distribution_mutate(value=self.height, mutation_rate=mutation_rate),
        )

    def mutatable_gene_count(self) -> int:
        return 4
