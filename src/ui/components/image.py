from typing import Optional
from numpy import random
from PIL.Image import Image

from genetic.attributes.position import Position
from genetic.attributes.size import Size
from genetic.mutation import normal_distribution_mutate
from genetic.recombination import intermediate_recombination
from ui.element import UIElement
from io import BytesIO
import base64

from ui.renderer import HTMLRenderer
from ui.util import horizontal_canvas_norm_to_pct, vertical_canvas_norm_to_pct

_base64_img_caches = {}


class ScaledImageView(UIElement):
    """
    A UI element that displays an image with a specified scale.
    Will infer size from image dimensions and scale.
    This will make sure that the image aspect ratio is always preserved.
    """

    image: Image
    scale: float

    MIN_SCALE = 0.01

    def __init__(
        self,
        image: Image,
        position: Optional[Position] = None,
        size: Optional[Size] = None,
        scale: Optional[float] = None,
    ):
        self.image = image
        self.scale = scale or random.uniform(0, 1)
        size = size or Size(width=self.scale, height=self.scale)
        super().__init__(position, size)

    @staticmethod
    def crossover(i1: "ScaledImageView", i2: "ScaledImageView") -> "ScaledImageView":
        # NOTE: We perform a reference wise check here as the instance gets passed along the children
        assert i1.image == i2.image, "Cannot crossover ImageViews with different images"
        new_position = Position.crossover(i1.position, i2.position)
        new_scale = max(
            ScaledImageView.MIN_SCALE, intermediate_recombination(i1.scale, i2.scale)
        )
        return ScaledImageView(image=i1.image, position=new_position, scale=new_scale)

    def mutate(self, mutation_rate: float):
        self.position.mutate(mutation_rate)
        self.scale = max(
            self.MIN_SCALE,
            normal_distribution_mutate(
                value=self.scale, mutation_rate=mutation_rate, i_min=0, i_max=1
            ),
        )
        self.size.width = self.scale
        self.size.height = self.scale

    def mutatable_gene_count(self) -> int:
        # Position + scale gene
        return self.position.mutatable_gene_count() + 1

    def to_html_element(self) -> str:
        x = horizontal_canvas_norm_to_pct(self.position.x)
        width = vertical_canvas_norm_to_pct(self.size.width)
        y = vertical_canvas_norm_to_pct(self.position.y)
        height = vertical_canvas_norm_to_pct(self.size.height)
        styles = {
            "left": f"{x}%",
            "top": f"{y}%",
            "width": f"{width}px",
            "height": f"{height}px",
        }
        img_id = id(self.image)
        if img_id in _base64_img_caches:
            img_str = _base64_img_caches[img_id]
        else:
            img_buffer = BytesIO()
            self.image.save(img_buffer, format="JPEG")
            img_str = f"data:image/jpeg;base64,{base64.b64encode(img_buffer.getvalue()).decode('utf-8')}"
            _base64_img_caches[img_id] = img_str

        return HTMLRenderer.get_styled_element(
            "img", styles, extra_attributes={"src": img_str}
        )
