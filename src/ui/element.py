from abc import ABC, abstractmethod
from typing import Optional

from genetic.attributes.position import Position
from genetic.attributes.size import Size
from genetic.reproducible import Reproducible


class UIElement(Reproducible, ABC):
    label: Optional[str]
    position: Position
    size: Size

    def __init__(
        self,
        label: Optional[str],
        position: Optional[Position] = None,
        size: Optional[Size] = None,
    ):
        self.label = label
        self.position = position or Position()
        self.size = size or Size()

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
        self.size.width = max(0, min(self.size.width, 1))
        self.size.height = max(0, min(self.size.height, 1))
        # Clamp position
        self.position.x = max(0, min(self.position.x, 1 - self.size.width))
        self.position.y = max(0, min(self.position.y, 1 - self.size.height))
