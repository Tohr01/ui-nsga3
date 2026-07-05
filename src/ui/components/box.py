from dataclasses import dataclass
from typing import Optional

from genetic.attributes.position import Position
from genetic.attributes.rgbcolor import RGBColor
from genetic.attributes.size import Size
from rendering.util import styles_dict_to_str
from ui.element import ElementConfig, UIElement


@dataclass
class BoxConfig(ElementConfig):
    enable_bg_color_crossover: bool = True
    enable_bg_color_mutation: bool = True


class Box(UIElement):
    """
    A simple UIElement representing a box with a background color, position and size.
    Every one of those genes/attributes can be mutated or/and crossed over.
    """

    bg_color: RGBColor
    config: BoxConfig  # type: ignore[override]

    def __init__(
        self,
        label: Optional[str] = None,
        position: Optional[Position] = None,
        size: Optional[Size] = None,
        bg_color: Optional[RGBColor] = None,
        config: BoxConfig = BoxConfig(),
    ):
        self.bg_color = bg_color or RGBColor()
        super().__init__(label, position, size, config)

    @staticmethod
    def crossover(i1: "Box", i2: "Box") -> "Box":
        new_position = (
            Position.crossover(i1.position, i2.position)
            if i1.config.enable_position_crossover
            else i1.position
        )

        new_size = (
            Size.crossover(i1.size, i2.size)
            if i1.config.enable_size_crossover
            else i1.size
        )

        new_bg_color = (
            RGBColor.crossover(i1.bg_color, i2.bg_color)
            if i1.config.enable_bg_color_crossover
            else i1.bg_color
        )

        return Box(i1.label, new_position, new_size, new_bg_color, i1.config)

    def mutate(self, mutation_rate: float):
        if self.config.enable_position_mutation:
            self.position.mutate(mutation_rate)
        if self.config.enable_size_mutation:
            self.size.mutate(mutation_rate)
        if self.config.enable_bg_color_mutation:
            self.bg_color.mutate(mutation_rate)

    def to_html_element(self) -> str:
        x, y = self.position.get_xy()
        w, h = self.size.get_wh()
        styles = {
            "left": f"{x * 100}%",
            "top": f"{y * 100}%",
            "width": f"{w * 100}%",
            "height": f"{h * 100}%",
            "background-color": self.bg_color.to_html_str(),
        }
        return f'<div style="{styles_dict_to_str(styles)}"></div>'
