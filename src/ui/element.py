from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from numpy import clip

from genetic.attributes.position import Position
from genetic.attributes.size import Size
from genetic.reproducible import Reproducible


@dataclass
class ElementConfig:
    # Indicating whether the ui element is a target for user interaction
    is_touch_target: bool = False

    #
    # Crossover settings
    #
    # NOTE: When one of the crossover settings is disabled the child
    # will inherit value from child one
    enable_position_crossover: bool = True
    enable_size_crossover: bool = True

    #
    # Mutation settings
    #
    enable_position_mutation: bool = True
    enable_size_mutation: bool = True


class UIElement(Reproducible, ABC):
    label: Optional[str]
    position: Position
    size: Size
    config: ElementConfig

    def __init__(
        self,
        label: Optional[str],
        position: Optional[Position] = None,
        size: Optional[Size] = None,
        config: ElementConfig = ElementConfig(),
    ):
        self.label = label
        self.position = position or Position()
        self.size = size or Size()
        self.config = config

    @abstractmethod
    def to_html_element(self) -> str:
        raise NotImplementedError(
            "to_html_element method must be implemented by subclass."
        )

    def clamp_to_canvas(self):
        """
        Clamps the position and size of the element to ensure it fits within the canvas.
        1. Clamp size first
        2. Clamp position based on the clamped size
        """
        # Clamp size
        self.size.width = clip(self.size.width, 0, 1)
        self.size.height = clip(self.size.height, 0, 1)
        # Clamp position
        self.position.x = clip(self.position.x, 0, 1 - self.size.width)
        self.position.y = clip(self.position.y, 0, 1 - self.size.height)
