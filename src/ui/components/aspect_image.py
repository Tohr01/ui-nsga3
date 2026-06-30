from copy import deepcopy
from dataclasses import dataclass
from typing import Optional

import numpy.random as random
from numpy import clip

from genetic.attributes.position import Position
from genetic.attributes.size import Size
from genetic.mutation import normal_distribution_mutate
from genetic.recombination import intermediate_recombination
from rendering.util import styles_dict_to_str
from ui.canvas_context import CanvasContext
from ui.element import ElementConfig, UIElement
from ui.enums import ImageType
from ui.util import img_path_to_base64_str


@dataclass
class AspectImageConfig(ElementConfig):
    image_type: ImageType = ImageType.OTHER


class AspectImage(UIElement):
    """
    An UIElement representing an image with a fixed aspect ratio.
    While mutating, crossover or initialization the object will ensure
    that the aspect ratio is preserved by only mutating the width and calculating the
    height based on the aspect ratio.
    """

    img_path: str
    aspect_ratio: float  # width / height
    config: AspectImageConfig  # type: ignore[override]

    def __init__(
        self,
        img_path: str,
        aspect_ratio: float,
        label: Optional[str],
        position: Optional[Position] = None,
        size: Optional[Size] = None,
        config: AspectImageConfig = AspectImageConfig(),
    ):
        self.img_path = img_path
        self.aspect_ratio = aspect_ratio
        if size is None:
            r_width = random.uniform(0, 1)
            size = self._size_from(r_width)

        super().__init__(label=label, position=position, size=size, config=config)

    def _size_from(self, width: float) -> Size:
        """
        Returns new Size object with given width and fitting height based on the aspect ratio
        based on the image and canvas aspect ratios.
        :param width: The width to use for the new Size object.
        :return: A new Size object
        """
        height = width * (CanvasContext.get_instance().aspect_ratio / self.aspect_ratio)
        return Size(width, height)

    @staticmethod
    def crossover(i1: "AspectImage", i2: "AspectImage") -> "AspectImage":
        # Crossover position
        new_position = (
            Position.crossover(i1.position, i2.position)
            if i1.config.enable_position_crossover
            else i1.position
        )
        # Crossover size
        # In order to retain aspect ratio we crossover the width and deduce the height
        if i1.config.enable_size_crossover:
            new_width = max(0, intermediate_recombination(i1.size.width, i2.size.width))
            new_size = i1._size_from(new_width)
        else:
            new_size = deepcopy(i1.size)

        return AspectImage(
            img_path=i1.img_path,
            aspect_ratio=i1.aspect_ratio,
            label=i1.label,
            position=new_position,
            size=new_size,
            config=i1.config,
        )

    def mutate(self, mutation_rate: float):
        if self.config.enable_position_mutation:
            self.position.mutate(mutation_rate)
        if self.config.enable_size_mutation:
            # Mutate width and deduce height to retain aspect ratio
            new_width = max(
                0,
                normal_distribution_mutate(
                    value=self.size.width, mutation_rate=mutation_rate
                ),
            )
            self.size = self._size_from(new_width)

    def clamp_to_canvas(self):
        """
        Clamp the position and size of the image to fit within the canvas while retaining the aspect ratio.
        1. If the size exceeds the canvas dimensions, scale it down to fit within the canvas
        while retaining the aspect ratio.
        2. Clamp the position
        """
        # Clamp size to fit within canvas; retaining aspect ratio
        if self.size.width > 1 or self.size.height > 1:
            scale = 1 / max(self.size.width, self.size.height)
            self.size.width *= scale
            self.size.height *= scale

        # Clamp position to fit within canvas
        self.position.x = clip(self.position.x, 0, 1 - self.size.width)
        self.position.y = clip(self.position.y, 0, 1 - self.size.height)

    def to_html_element(self) -> str:
        # Read image using pillow and convert to base64 string
        styles = {
            "position": "absolute",
            "left": f"{self.position.x * 100}%",
            "top": f"{self.position.y * 100}%",
            "height": f"{self.size.height * 100}%",
            "width": f"{self.size.width * 100}%",
        }
        return f'<img src="{img_path_to_base64_str(self.img_path)}" style="{styles_dict_to_str(styles)}" />'
