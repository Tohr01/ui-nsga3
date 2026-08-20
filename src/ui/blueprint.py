import uuid
from dataclasses import dataclass, field
from typing import Type

import numpy as np

from scoring.scorer import Scorer
from ui.components.placeholder_container import PlaceholderContainer
from ui.container import Container
from ui.element import UIElement


@dataclass(kw_only=True, frozen=True)
class BlueprintContainer:
    """
    Blueprint for Container containing required Elements (or other BlueprintContainers) and Scorers.
    """

    label: str
    blueprint_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    elements: list["BlueprintContainer" | tuple[Type[UIElement], dict]]
    scorers: list[tuple[Scorer, float]]
    additional_constraints: list[Scorer] = field(default_factory=list)

    flattend_elements: list[tuple[Type[UIElement], dict]] = field(init=False)
    container_subelement_count: dict[str, int] = field(init=False)

    def __post_init__(self):
        """
        After initialization will two things:
        1.  Will flatten the elements list by replacing any BlueprintContainer with a PlaceholderContainer and
            keeping the other elements as they are.
            The flatted_elements array will have the the following format:
            - If the element is a BlueprintContainer:
              (PlaceholderContainer, {"label": element.label, "blueprint_id": BlueprintContainer.blueprint_id})
            - If the element is a tuple of (UIElement type, args):
              (UIElement type, init args)
        2. Will count the number of subelements in each BlueprintContainer and store it in a dictionary with the blueprint_id as the key
           and the count as the value.
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

        container_subelement_count = {}
        for element in self.elements:
            if isinstance(element, BlueprintContainer):
                container_subelement_count[element.blueprint_id] = (
                    element.count_subelements()
                )

        # Bypass frozen
        object.__setattr__(
            self, "container_subelement_count", container_subelement_count
        )

    def count_subelements(self) -> int:
        """
        Recursivly count the number of subelements in the blueprint
        :return: The total number of (nested) subelements in the blueprint
        """
        element_count = 0
        for element in self.elements:
            if isinstance(element, BlueprintContainer):
                element_count += element.count_subelements()
            else:
                element_count += 1
        return element_count

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

    def get_scorers(self) -> list[Scorer]:
        """
        Returns a list of the scorers in the blueprint.
        :return: list of Scorer instances
        """
        return [scorer for scorer, _ in self.scorers]

    def get_scorer_class_names(self) -> list[str]:
        """
        Returns a list of the class names of the scorers in the blueprint.
        :return: list of scorer class names
        """
        return [scorer.__class__.__name__ for scorer, _ in self.scorers]

    def get_normalized_scorer_weight_arr(self) -> np.ndarray:
        """
        Returns a numpy array of the normalized weights of the scorers.
        Higher weight is more important and sum(weights) == 1.0
        :return: numpy array of normalized weights
        """
        weights = np.array([weight for _, weight in self.scorers], dtype=float)
        weights_sum = weights.sum()
        return weights / weights_sum if weights_sum != 0 else weights


@dataclass(kw_only=True, frozen=True)
class RootBlueprint(BlueprintContainer):
    """
    Subclass of BlueprintContainer. Should be at the root of every interface definition.
    Allows definition of the canvas dimensions in pixels.
    """

    width_px: float
    height_px: float
    label: str = "Interface Root"
    global_constraints: list[Scorer] = field(default_factory=list)
