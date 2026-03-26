from genetic.reproducible import Reproducible
from ui.element import UIElement


class Container(Reproducible):
    container_id: int
    # TODO: Maybe use relative units instantly
    width_px: float
    width_aspect_ratio: float
    height_px: float
    height_aspect_ratio: float
    label: str
    elements: list[UIElement]

    def __init__(
        self,
        container_id: int,
        width_px: float,
        height_px: float,
        label: str,
        elements: list[UIElement],
    ):
        self.container_id = container_id
        self.width_px = width_px
        self.height_px = height_px
        # TODO: Maybe do not calculate always on init but precalulate in sampling
        self.width_aspect_ratio = width_px / max(height_px, width_px)
        self.height_aspect_ratio = height_px / max(width_px, height_px)
        self.label = label
        self.elements = elements

    @staticmethod
    def crossover(i1: "Container", i2: "Container") -> "Container":
        new_elements: list[UIElement] = []
        assert i1.container_id == i2.container_id, (
            "Crossover can only be performed on Containers with the same container_id."
        )
        for element1, element2 in zip(i1.elements, i2.elements):
            assert type(element1) is type(element2), (
                "Crossover can only be performed on Containers with the same elements."
            )
            new_elements.append(type(element1).crossover(element1, element2))
        return Container(
            i1.container_id, i1.width_px, i1.height_px, i1.label, new_elements
        )

    def mutate(self, mutation_rate: float):
        for element in self.elements:
            element.mutate(mutation_rate)

    def mutatable_gene_count(self) -> int:
        return sum(element.mutatable_gene_count() for element in self.elements)

    def __repr__(self) -> str:
        elements_str = "\n".join(type(element).__name__ for element in self.elements)
        return f"""--- Container "{self.label}" - {self.container_id} ---
{elements_str}
        """
