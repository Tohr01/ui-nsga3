from typing import Optional
from genetic.mutation import normal_distribution_mutate
from genetic.recombination import intermediate_recombination
from genetic.reproducible import Reproducible
from numpy import clip, random


class RGBColor(Reproducible):
    r: int
    g: int
    b: int

    def __init__(
        self, r: Optional[int] = None, g: Optional[int] = None, b: Optional[int] = None
    ):
        self.r, self.g, self.b = (self._init_channel(c) for c in (r, g, b))

    def _init_channel(self, channel: Optional[int]) -> int:
        assert channel is None or (0 <= channel <= 255), (
            "Color channel must be between 0 and 255"
        )

        return channel if channel is not None else random.randint(0, 256)

    @staticmethod
    def crossover(i1: "RGBColor", i2: "RGBColor") -> "RGBColor":
        new_r, new_g, new_b = (
            clip(intermediate_recombination(getattr(i1, c), getattr(i2, c)), 0, 255)
            for c in ("r", "g", "b")
        )
        return RGBColor(int(new_r), int(new_g), int(new_b))

    def mutate(self, mutation_rate: float):
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

    # NOTE: This is not in a overridden method of reproducible
    def to_html_str(self) -> str:
        return f"rgb({self.r}, {self.g}, {self.b})"
