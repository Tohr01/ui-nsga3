from genetic.mutation import normal_distribution_mutate
from genetic.recombination import intermediate_recombination
from genetic.reproducible import Reproducible
import numpy.random
from numpy import clip


class RGBColor(Reproducible):
    r: int
    g: int
    b: int

    def __init__(self, r: int, g: int, b: int):
        assert 0 <= r <= 255, "Red value must be between 0 and 255"
        assert 0 <= g <= 255, "Green value must be between 0 and 255"
        assert 0 <= b <= 255, "Blue value must be between 0 and 255"
        self.r = r
        self.g = g
        self.b = b

    @staticmethod
    def random() -> "RGBColor":
        return RGBColor(
            r=numpy.random.randint(0, 256),
            g=numpy.random.randint(0, 256),
            b=numpy.random.randint(0, 256),
        )

    @staticmethod
    def crossover(i1: "RGBColor", i2: "RGBColor") -> "RGBColor":
        new_r, new_g, new_b = (
            clip(intermediate_recombination(getattr(i1, c), getattr(i2, c)), 0, 255)
            for c in ("r", "g", "b")
        )
        return RGBColor(int(new_r), int(new_g), int(new_b))

    def mutate(self, mutation_rate: float):
        mutation_rate /= 3
        for channel in ("r", "g", "b"):
            mutated_channel = clip(
                normal_distribution_mutate(
                    value=getattr(self, channel),
                    mutation_rate=mutation_rate,
                    i_min=0,
                    i_max=255,
                ),
                0,
                255,
            )
            setattr(self, channel, int(mutated_channel))

    def mutatable_gene_count(self) -> int:
        return 3

    def to_html_str(self) -> str:
        return f"rgb({self.r}, {self.g}, {self.b})"
