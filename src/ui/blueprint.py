import uuid
from dataclasses import dataclass, field
from typing import Type

from scoring.scorer import Scorer
from ui.components.placeholder_container import PlaceholderContainer
from ui.container import Container
from ui.element import UIElement


@dataclass(kw_only=True, frozen=True)
class BlueprintContainer:
    label: str
    blueprint_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    elements: list["BlueprintContainer" | tuple[Type[UIElement], dict]]
    scorers: list[tuple[Scorer, float]]

    flattend_elements: list[tuple[Type[UIElement], dict]] = field(init=False)

    def __post_init__(self):
        """
        Will flatten the elements list by replacing any BlueprintContainer with a PlaceholderContainer and keeping the other elements as they are.
        The flatted_elements array will have the the following format:
        If the element is a BlueprintContainer:
        (PlaceholderContainer, {"label": element.label, "blueprint_id": BlueprintContainer.blueprint_id})
        If the element is a tuple of (UIElement type, args):
        (UIElement type, init args)
        """
        flattend_elements = []
        for element in self.elements:
            if isinstance(element, BlueprintContainer):
                flattend_elements.append(
                    (
                        PlaceholderContainer,
                        {"label": element.label, "blueprint_id": element.blueprint_id},
                    )
                )
            else:
                flattend_elements.append(element)
        # Bypass frozen
        object.__setattr__(self, "flattend_elements", flattend_elements)

    def get_new_container(self, width_px: float, height_px: float) -> Container:
        """
        Returns a new Container instance based on the blueprint with the given dimensions.
        """
        return Container(
            blueprint_id=self.blueprint_id,
            width_px=width_px,
            height_px=height_px,
            label=self.label,
            elements=[
                element_type(**element_args)
                for element_type, element_args in self.flattend_elements
            ],
        )


@dataclass(kw_only=True, frozen=True)
class RootBlueprint(BlueprintContainer):
    width_px: float
    height_px: float
    label: str = "Interface Root"
