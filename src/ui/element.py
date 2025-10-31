from abc import ABC, abstractmethod
from genetic.attributes.rect import Rect
from genetic.reproducible import Reproducible


class UIElement(Reproducible, ABC):
    bbox: Rect

    def __init__(self, bbox: Rect):
        self.bbox = bbox

    @abstractmethod
    def to_html_element(self) -> str:
        raise NotImplementedError(
            "to_html_element method must be implemented by subclass."
        )
