from constants import CANVAS_ASPECT_RATIO_X, CANVAS_ASPECT_RATIO_Y
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
        x_center = 0.5
        y_center = 0.5

        weighted_x_sum = 0
        weighted_y_sum = 0
        total_area = 0
        for element in ui.elements:
            x, y = element.position.get_xy()
            w, h = element.size.get_wh()
            area = element.size.visual_area()
            x_center_elem = x + w / 2
            y_center_elem = y + h / 2
            total_area += area
            weighted_x_sum += area * x_center_elem
            weighted_y_sum += area * y_center_elem

        # Compute the center of mass of the layout
        # Set to center if total_area is 0 to avoid division by zero
        # Meaning that there is basically a equilibirium at center
        x_0 = weighted_x_sum / total_area if total_area != 0 else x_center
        y_0 = weighted_y_sum / total_area if total_area != 0 else y_center

        em_x = (x_center - x_0) * CANVAS_ASPECT_RATIO_X
        em_y = (y_center - y_0) * CANVAS_ASPECT_RATIO_Y

        # TODO: Maybe return (em_x + em_y) / 2

        # Return the distance from perfect equilibrium (0, 0) as penalty
        return sqrt(em_x**2 + em_y**2)  
