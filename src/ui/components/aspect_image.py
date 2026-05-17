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
from ui.element import ElementConfig, UIElement
from ui.util import img_path_to_base64_str


@dataclass
class AspectImageConfig(ElementConfig):
    pass


class AspectImage(UIElement):
    img_path: str
    config: AspectImageConfig  # type: ignore[override]
    aspect_ratio: float  # width / height

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
            r_height = random.uniform(0, 1)
            size = self._size_from(r_height)

        super().__init__(label=label, position=position, size=size, config=config)

    def _size_from(self, height: float) -> Size:
        """
        Returns new Size object with given height and fitting width based on the aspect ratio.
        :param height: The height to use for the new Size object.
        :return: A new Size object
        """
        width = height * self.aspect_ratio
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
        # In order to retain aspect ratio we crossover the height and deduce the width
        if i1.config.enable_size_crossover:
            new_height = max(
                0, intermediate_recombination(i1.size.height, i2.size.height)
            )
            new_size = i1._size_from(new_height)
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
            # Mutate height and deduce width to retain aspect ratio
            new_height = max(
                0,
                normal_distribution_mutate(
                    value=self.size.height, mutation_rate=mutation_rate
                ),
            )
            self.size = self._size_from(new_height)

    def clamp_to_canvas(self):
        # Clamp size to fit within canvas; retaining aspect ratio
        if self.size.width > 1 or self.size.height > 1:
            # One dimension is larger than canvas
            non_zero_dimensions_scales = [
                d for d in [self.size.width, self.size.height] if d > 0
            ]
            if non_zero_dimensions_scales:
                scale = min(1 / d for d in non_zero_dimensions_scales)
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
            "aspect-ratio": f"{self.aspect_ratio}",
        }
        return f'<img src={img_path_to_base64_str(self.img_path)} style="{styles_dict_to_str(styles)}" />'
