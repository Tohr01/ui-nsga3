from typing import Optional, cast

from bs4 import Tag

from genetic.attributes.position import Position
from genetic.attributes.size import Size
from rendering.util import new_bs4_tag, styles_dict_to_str
from ui.element import UIElement


class PlaceholderContainer(UIElement):
    """
    The placeholder container is a special UIElement that is used to represent another container
    for optimization. After optimization is done the placeholder may be replaced with the actual container.
    """

    blueprint_id: str

    # NOTE: We do not supply an element config for placeholder as it is not directly
    # defined in the blueprint and things like mutation behavior should not be changed.
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
        # NOTE: Ignore self.config
        self.position.mutate(mutation_rate)
        self.size.mutate(mutation_rate)

    def to_html_element(self) -> Tag:
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
        div = new_bs4_tag("div", style=styles_dict_to_str(styles))
        return div
