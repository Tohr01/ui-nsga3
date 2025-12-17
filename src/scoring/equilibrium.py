from constants import CANVAS_HEIGHT_NORM, CANVAS_WIDTH_NORM
from genetic.ui import UserInterface
from scoring.scorer import Scorer
from math import sqrt


class EquilibriumScorer(Scorer):
    """
    Scores a UI based on the equilibrium of its elements.
    Forumla is based on the paper "Aesthetic Measures for Assessing Graphic Screens"
    See 3.2 https://www.researchgate.net/publication/220587460_Aesthetic_Measures_for_Assessing_Graphic_Screens
    """

    def score(self, ui: UserInterface) -> float:
        x_center = CANVAS_WIDTH_NORM / 2
        y_center = CANVAS_HEIGHT_NORM / 2
        element_areas = []
        element_x_positions = []
        element_y_positions = []
        for element in ui.elements:
            pos = element.position
            size = element.size
            element_areas.append(size.area())
            x_center_elem = pos.x + size.width / 2
            y_center_elem = pos.y + size.height / 2
            element_x_positions.append(x_center_elem)
            element_y_positions.append(y_center_elem)

        weighted_x_sum = sum(
            area * x_pos for area, x_pos in zip(element_areas, element_x_positions)
        )
        weighted_y_sum = sum(
            area * y_pos for area, y_pos in zip(element_areas, element_y_positions)
        )
        total_area = sum(element_areas)

        # Compute the center of mass of the layout
        # Set to center if total_area is 0 to avoid division by zero
        # Meaning that there is basically a equilibirium at center
        x_0 = weighted_x_sum / total_area if total_area != 0 else x_center
        y_0 = weighted_y_sum / total_area if total_area != 0 else y_center

        em_x = x_center - x_0
        em_y = y_center - y_0

        return -sqrt(em_x**2 + em_y**2)
