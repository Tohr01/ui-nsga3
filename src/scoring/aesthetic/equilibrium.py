from math import sqrt

from scoring.scorer import Scorer
from ui.container import Container


class EquilibriumScorer(Scorer):
    """
    Scores a Container based on the equilibrium of its elements.

    References:
    -----------
    [1] D. Ngo, A. Samsudin und R. Abdullah,
        „Aesthetic Measures for Assessing Graphic Screens“,
        Journal Of Information Science And Engineering,
        Bd. 16, Nr. 1, S. 97–116, Jan. 2000,
        doi: 10.6688/jise.2000.16.1.4.
    """

    MAX_PENALTY = sqrt(0.5**2 + 0.5**2)

    def score(self, container: Container) -> float:
        # NOTE: WHEN CHANGING THIS CHANGE NORMALIZATION
        x_center = 0.5
        y_center = 0.5

        weighted_x_sum = 0
        weighted_y_sum = 0
        total_area = 0
        for element in container.elements:
            x, y = element.position.get_xy()
            w, h = element.size.get_wh()
            area = element.size.area()
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

        em_x = x_center - x_0
        em_y = y_center - y_0

        # Return the distance from perfect equilibrium (0, 0) as penalty
        return sqrt(em_x**2 + em_y**2) / self.MAX_PENALTY  # Normalize to [0, 1]
