from genetic.attributes.rect import Rect
from genetic.attributes.rgbcolor import RGBColor
from ui.element import UIElement
from ui.renderer import HTMLRenderer


class Box(UIElement):
    bg_color: RGBColor

    def __init__(self, bbox: Rect, bg_color: RGBColor):
        self.bg_color = bg_color
        super().__init__(bbox)

    @staticmethod
    def random() -> "Box":
        return Box(Rect.random(), RGBColor.random())

    @staticmethod
    def crossover(i1: "Box", i2: "Box") -> "Box":
        new_bbox = Rect.crossover(i1.bbox, i2.bbox)
        new_bg_color = RGBColor.crossover(i1.bg_color, i2.bg_color)
        return Box(new_bbox, new_bg_color)

    def mutate(self, mutation_rate: float):
        bbox_mutation_rate = mutation_rate * (
            self.bbox.mutatable_gene_count() / self.mutatable_gene_count()
        )
        bg_color_mutation_rate = (
            mutation_rate
            * self.bg_color.mutatable_gene_count()
            / self.mutatable_gene_count()
        )

        self.bbox.mutate(bbox_mutation_rate)
        self.bg_color.mutate(bg_color_mutation_rate)

    def mutatable_gene_count(self) -> int:
        return self.bbox.mutatable_gene_count() + self.bg_color.mutatable_gene_count()

    def to_html_element(self) -> str:
        styles = {
            "left": f"{self.bbox.x * 100}%",
            "top": f"{self.bbox.y * 100}%",
            "width": f"{self.bbox.width * 100}%",
            "height": f"{self.bbox.height * 100}%",
            "background-color": self.bg_color.to_html_str(),
        }
        return HTMLRenderer.get_styled_element("div", styles)
