from dataclasses import dataclass
from typing import Optional

from genetic.attributes.position import Position
from genetic.attributes.size import Size
from rendering.util import styles_dict_to_str
from ui.components.aspect_image import ImageType
from ui.element import ElementConfig, UIElement
from ui.util import img_path_to_base64_str


@dataclass
class ConverImageConfig(ElementConfig):
    image_type: ImageType = ImageType.OTHER


class CoverImage(UIElement):
    img_path: str
    config: ConverImageConfig  # type: ignore[override]

    def __init__(
        self,
        img_path: str,
        label: Optional[str] = None,
        position: Optional[Position] = None,
        size: Optional[Size] = None,
        config: ConverImageConfig = ConverImageConfig(),
    ):
        self.img_path = img_path
        super().__init__(label=label, position=position, size=size, config=config)

    @staticmethod
    def crossover(i1: "CoverImage", i2: "CoverImage") -> "CoverImage":
        # Crossover position
        new_position = (
            Position.crossover(i1.position, i2.position)
            if i1.config.enable_position_crossover
            else i1.position
        )
        # Crossover size
        new_size = (
            Size.crossover(i1.size, i2.size)
            if i1.config.enable_size_crossover
            else i1.size
        )
        return CoverImage(
            img_path=i1.img_path,
            label=i1.label,
            position=new_position,
            size=new_size,
            config=i1.config,
        )

    def mutate(self, mutation_rate: float):
        if self.config.enable_position_mutation:
            self.position.mutate(mutation_rate)
        if self.config.enable_size_mutation:
            self.size.mutate(mutation_rate)

    def to_html_element(self) -> str:
        x, y = self.position.get_xy()
        w, h = self.size.get_wh()
        styles = {
            "position": "absolute",
            "left": f"{x * 100}%",
            "top": f"{y * 100}%",
            "width": f"{w * 100}%",
            "height": f"{h * 100}%",
            "object-fit": "cover",
        }
        return f'<img src="{img_path_to_base64_str(self.img_path)}" style="{styles_dict_to_str(styles)}" />'
