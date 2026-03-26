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
