from typing import Optional

from genetic.attributes.position import Position
from genetic.attributes.size import Size
from ui.element import UIElement
from ui.renderer import HTMLRenderer


class PlaceholderContainer(UIElement):
    container_id: int

    def __init__(
        self,
        container_id: int,
        label: str,
        position: Optional[Position] = None,
        size: Optional[Size] = None,
    ):
        self.container_id = container_id
        super().__init__(label, position, size)

    @staticmethod
    def crossover(
        i1: "PlaceholderContainer", i2: "PlaceholderContainer"
    ) -> "PlaceholderContainer":
        assert i1.container_id == i2.container_id, (
            "Crossover can only be performed on PlaceholderContainers with the same container_id."
        )
        new_position = Position.crossover(i1.position, i2.position)
        new_size = Size.crossover(i1.size, i2.size)
        return PlaceholderContainer(i1.container_id, i1.label, new_position, new_size)

    def mutate(self, mutation_rate: float):
        self.position.mutate(mutation_rate)
        self.size.mutate(mutation_rate)

    def mutatable_gene_count(self) -> int:
        return self.position.mutatable_gene_count() + self.size.mutatable_gene_count()

    def to_html_element(self) -> str:
        x, y = self.position.get_xy()
        w, h = self.size.get_wh()
        styles = {
            "left": f"{x * 100}%",
            "top": f"{y * 100}%",
            "width": f"{w * 100}%",
            "height": f"{h * 100}%",
            "background-color": "transparent",
            "border": "2px dashed black",
        }
        return HTMLRenderer.get_styled_element(
            "div", styles, extra_attributes={"label": self.label}
        )
