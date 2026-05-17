from enum import StrEnum

from scoring.scorer import Scorer
from ui.container import Container


class ScreenSpaceDimensionMode(StrEnum):
    WIDTH = "width"
    HEIGHT = "height"
    BOTH = "both"


class ScreenSpaceUtitizationScorer(Scorer):
    """
    This scorer penalizes unused screen space (given a mode of width, height or area (width*height))
    by calculating the utilization of each element in the container (and returning the average)

    Based on source: https://www.nngroup.com/articles/utilize-available-screen-space/
    Latest accessed: 2026-05-13
    """

    screen_space_dimension_mode: ScreenSpaceDimensionMode

    def __init__(
        self,
        screen_space_dimension_mode: ScreenSpaceDimensionMode = ScreenSpaceDimensionMode.BOTH,
    ) -> None:
        self.screen_space_dimension_mode = screen_space_dimension_mode

    def score(self, container: Container) -> float:
        penalty = 0.0
        for element in container.elements:
            w, h = element.size.get_wh()
            match self.screen_space_dimension_mode:
                case ScreenSpaceDimensionMode.WIDTH:
                    area_utilization = w
                case ScreenSpaceDimensionMode.HEIGHT:
                    area_utilization = h
                case ScreenSpaceDimensionMode.BOTH:
                    area_utilization = w * h

            penalty += 1.0 - area_utilization

        if len(container.elements) > 0:
            penalty /= len(container.elements)

        return penalty
