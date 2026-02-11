from typing import Optional
from genetic.attributes.position import Position
from genetic.attributes.rgbcolor import RGBColor
from genetic.attributes.size import Size
from ui.element import UIElement
from ui.renderer import HTMLRenderer


class Box(UIElement):
    bg_color: RGBColor

    def __init__(
        self,
        position: Optional[Position] = None,
        size: Optional[Size] = None,
        bg_color: Optional[RGBColor] = None,
    ):
        self.bg_color = bg_color or RGBColor()
        super().__init__(position, size)

    @staticmethod
    def crossover(i1: "Box", i2: "Box") -> "Box":
        new_position = Position.crossover(i1.position, i2.position)
        new_size = Size.crossover(i1.size, i2.size)
        new_bg_color = RGBColor.crossover(i1.bg_color, i2.bg_color)
        return Box(new_position, new_size, new_bg_color)

    def mutate(self, mutation_rate: float):
        self.position.mutate(mutation_rate)
        self.size.mutate(mutation_rate)
        self.bg_color.mutate(mutation_rate)

    def mutatable_gene_count(self) -> int:
        return (
            self.position.mutatable_gene_count()
            + self.size.mutatable_gene_count()
            + self.bg_color.mutatable_gene_count()
        )

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
        return HTMLRenderer.get_styled_element("div", styles)
