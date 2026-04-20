from typing import Optional, cast

from genetic.attributes.position import Position
from genetic.attributes.size import Size
from rendering.util import attributes_dict_to_str, styles_dict_to_str
from ui.element import UIElement


class PlaceholderContainer(UIElement):
    blueprint_id: str

    def __init__(
        self,
        blueprint_id: str,
        label: str,
        position: Optional[Position] = None,
        size: Optional[Size] = None,
    ):
        self.blueprint_id = blueprint_id
        super().__init__(label, position, size)

    @staticmethod
    def crossover(
        i1: "PlaceholderContainer", i2: "PlaceholderContainer"
    ) -> "PlaceholderContainer":
        assert i1.blueprint_id == i2.blueprint_id, (
            "Crossover can only be performed on PlaceholderContainers with the same blueprint_id"
        )
        new_position = Position.crossover(i1.position, i2.position)
        new_size = Size.crossover(i1.size, i2.size)
        return PlaceholderContainer(
            i1.blueprint_id, cast(str, i1.label), new_position, new_size
        )

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
            "position": "absolute",
        }
        attributes = {
            "label": cast(str, self.label),
            "style": styles_dict_to_str(styles),
        }
        return f"<div {attributes_dict_to_str(attributes)}></div>"
