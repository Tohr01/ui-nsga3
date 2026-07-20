from typing import Optional

from bs4 import Tag

from genetic.reproducible import Reproducible
from rendering.util import new_bs4_tag, styles_dict_to_str
from ui.components.placeholder_container import PlaceholderContainer
from ui.element import UIElement


class Container(Reproducible):
    """
    The Container holds a list of UIElements and is the main individual in the genetic algorithm.
    A Container is usually synthesized from a BlueprintContainer.
    """

    blueprint_id: str

    # Absolute dimensions of container canvas in pixels
    width_px: float
    height_px: float

    label: str
    elements: list[UIElement]

    def __init__(
        self,
        blueprint_id: str,
        width_px: float,
        height_px: float,
        label: str,
        elements: list[UIElement],
    ):
        self.x, self.y = None, None
        self.blueprint_id = blueprint_id
        self.width_px = width_px
        self.height_px = height_px
        self.label = label
        self.elements = elements

    @staticmethod
    def crossover(i1: "Container", i2: "Container") -> "Container":
        new_elements: list[UIElement] = []
        assert i1.blueprint_id == i2.blueprint_id, (
            "Crossover can only be performed on Containers with the same blueprint_id"
        )
        for element1, element2 in zip(i1.elements, i2.elements):
            if type(element1) is not type(element2):
                raise TypeError(
                    f"Can only crossover elements of same type. Got {type(element1)} and {type(element2)}."
                )

            new_elements.append(type(element1).crossover(element1, element2))
        return Container(
            i1.blueprint_id, i1.width_px, i1.height_px, i1.label, new_elements
        )

    def mutate(self, mutation_rate: float):
        for element in self.elements:
            element.mutate(mutation_rate)

    def __repr__(self) -> str:
        elements_str = "\n".join(type(element).__name__ for element in self.elements)
        return f"""--- Container "{self.label}" - {self.blueprint_id} ---
{elements_str}
        """

    def to_html_element(
        self,
        containers: Optional[dict[str, "Container"]] = None,
        x: Optional[float] = None,
        y: Optional[float] = None,
        width: Optional[float] = None,
        height: Optional[float] = None,
    ) -> Tag:
        """
        Renders the container and its elements a HTML string. If the container contains PlaceholderContainers,
        they will be replaced with the optimized containers from the containers dictionary if they exist.
        If any element has a label attribute it will be added as the data-label attribute to the respective html string.

        :param containers: A dictionary of blueprint_id to Container instances. Used to replace PlaceholderContainers
        :param x: The x position of the container in percentage (0-1).
        :param y: The y position of the container in percentage (0-1). If None, the container will be positioned at 0.
        :param width: The width of the container in percentage (0-1). If None, the container will be sized to 100%.
        :param height: The height of the container in percentage (0-1). If None, the container will be sized to 100%.
        :return: bs4 Tag containing the container and its elements as HTML.
        """
        styles = {
            "x": f"{(x or 0) * 100}%",
            "y": f"{(y or 0) * 100}%",
            "height": f"{(height or 1) * 100}%",
            "width": f"{(width or 1) * 100}%",
        }
        if x is not None:
            styles["left"] = f"{x * 100}%"
        if y is not None:
            styles["top"] = f"{y * 100}%"
        if width is not None:
            styles["width"] = f"{width * 100}%"
        if height is not None:
            styles["height"] = f"{height * 100}%"

        div = new_bs4_tag("div", style=styles_dict_to_str(styles))
        div["data-label"] = self.label

        for element in self.elements:
            # Check whether element is a placeholder container and if the user provided the Container
            # Recursively get the html str of the container
            if (
                containers
                and isinstance(element, PlaceholderContainer)
                and element.blueprint_id in containers
            ):
                container = containers[element.blueprint_id]
                html_element = container.to_html_element(
                    containers=containers,
                    x=element.position.x,
                    y=element.position.y,
                    width=element.size.width,
                    height=element.size.height,
                )
            else:
                html_element = element.to_html_element()

            if element.label:
                html_element["data-label"] = element.label

            div.append(html_element)

        return div
