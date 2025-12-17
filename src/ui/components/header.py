from genetic.attributes.position import Position
from genetic.attributes.size import Size
from ui.element import UIElement
from ui.renderer import HTMLRenderer
from ui.util import horizontal_canvas_norm_to_pct, vertical_canvas_norm_to_pct


class Header(UIElement):
    def to_html_element(self) -> str:
        # FIX: Make actual good placeholder
        x = horizontal_canvas_norm_to_pct(self.position.x)
        width = horizontal_canvas_norm_to_pct(self.size.width)
        y = vertical_canvas_norm_to_pct(self.position.y)
        height = vertical_canvas_norm_to_pct(self.size.height)
        styles = {
            "left": f"{x}%",
            "top": f"{y}%",
            "width": f"{width}%",
            "height": f"{height}%",
            "background-color": "#000",
        }
        return HTMLRenderer.get_styled_element("div", styles)
