from typing import Optional
from genetic.attributes.position import Position
from genetic.attributes.rgbcolor import RGBColor
from genetic.attributes.size import Size
from ui.element import UIElement


class Button(UIElement):
    bg_color: RGBColor
    text: str
    text_color: RGBColor

    def __init__(
        self,
        position: Optional[Position] = None,
        size: Optional[Size] = None,
        bg_color: Optional[RGBColor] = None,
        text: str = "Button",
        text_color: Optional[RGBColor] = None,
    ):
        self.bg_color = bg_color or RGBColor()
        self.text = text
        self.text_color = text_color or RGBColor()
        super().__init__(position, size)

    @staticmethod
    def crossover(i1: "Button", i2: "Button") -> "Button":
        assert i1.text == i2.text, (
            "Crossover can only be performed between Buttons with the same text."
        )
        new_position = Position.crossover(i1.position, i2.position)
        new_size = Size.crossover(i1.size, i2.size)
        new_bg_color = RGBColor.crossover(i1.bg_color, i2.bg_color)
        return Button(new_position, new_size, new_bg_color, i1.text)

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
        styles = {
            "left": f"{self.position.x * 100}%",
            "top": f"{self.position.y * 100}%",
            "width": f"{self.size.width * 100}%",
            "height": f"{self.size.height * 100}%",
            "background-color": self.bg_color.to_html_str(),
            "color": self.text_color.to_html_str(),
            "font-size": "16px",  # TODO: make this adjustable or mutatable
            "cursor": "pointer",
            "border": "none",
            "padding": "0",
            "overflow": "hidden",
        }
        style_str = "; ".join(f"{k}: {v}" for k, v in styles.items())
        return f'<button style="{style_str}">{self.text}</button>'
