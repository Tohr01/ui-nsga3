from dataclasses import dataclass, field
from typing import Type

from scoring.content import ContentScorer
from scoring.footer import FooterScorer
from scoring.header import HeaderScorer
from scoring.scorer import Scorer
from ui.components.placeholder_container import PlaceholderContainer
from ui.container import Container
from ui.element import UIElement


@dataclass(kw_only=True, frozen=True)
class BlueprintContainer:
    label: str
    elements: list["BlueprintContainer" | tuple[Type[UIElement], dict]]
    scorers: list[tuple[Type[Scorer], float]]

    flattend_elements: list[tuple[Type[UIElement], dict]] = field(init=False)

    def __post_init__(self):
        """
        Will flatten the elements list by replacing any BlueprintContainer with a PlaceholderContainer and keeping the other elements as they are.
        The flatted_elements array will have the the following format:
        If the element is a BlueprintContainer:
        (PlaceholderContainer, {"label": element.label, "container_id": id(element)})
        If the element is a tuple of (UIElement type, args):
        (UIElement type, init args)
        """
        flattend_elements = []
        for element in self.elements:
            if isinstance(element, BlueprintContainer):
                flattend_elements.append(
                    (
                        PlaceholderContainer,
                        {"label": element.label, "container_id": id(element)},
                    )
                )
            else:
                flattend_elements.append(element)
        # Bypass frozen
        object.__setattr__(self, "flattend_elements", flattend_elements)

    def get_new_container(self, width_px: float, height_px: float) -> Container:
        return Container(
            container_id=id(self),
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


interface_blueprint = RootBlueprint(
    width_px=1920,
    height_px=1080,
    label="Interface",
    elements=[
        BlueprintContainer(label="Header", elements=[], scorers=[]),
        BlueprintContainer(label="Content", elements=[], scorers=[]),
        BlueprintContainer(label="Footer", elements=[], scorers=[]),
    ],
    scorers=[(HeaderScorer, 1.0), (FooterScorer, 1.0), (ContentScorer, 1.0)],
)


def construct_optimization_queue(
    blueprint: BlueprintContainer,
) -> list[BlueprintContainer]:
    """
    Performs a breadth-first search on the blueprint object to construct a queue of BlueprintContainer objects. The BFS treats the BlueprintContainers as nodes and the elements as leafs.
    :param blueprint: The root BlueprintContainer object to start the BFS from.
    :return: A list of BlueprintContainer objects in the order they were visited in the BFS.
    """
    queue = [blueprint]
    optimization_queue: list[BlueprintContainer] = []
    while queue:
        current = queue.pop(0)
        optimization_queue.append(current)
        for element in current.elements:
            if isinstance(element, BlueprintContainer):
                queue.append(element)

    return optimization_queue
