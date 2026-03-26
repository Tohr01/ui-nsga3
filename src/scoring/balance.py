from math import sqrt

from scoring.scorer import Scorer
from ui.container import Container


class BalanceScorer(Scorer):
    """
    Scores a Container based on the balance of its elements.
    Forumla is based on the paper "Aesthetic Measures for Assessing Graphic Screens"
    See 3.1 https://www.researchgate.net/publication/220587460_Aesthetic_Measures_for_Assessing_Graphic_Screens
    """

    def score(self, container: Container) -> float:
        x_center = 0.5
        y_center = 0.5
        wl, wr, wt, wb = 0, 0, 0, 0
        for element in container.elements:
            pos = element.position
            size = element.size

            area = size.visual_area()
            cx = pos.x + size.width / 2
            cy = pos.y + size.height / 2

            dx = abs(x_center - cx) * container.width_aspect_ratio
            dy = abs(y_center - cy) * container.height_aspect_ratio
            if cx < x_center:
                wl += area * dx
            elif cx > x_center:
                wr += area * dx

            if cy < y_center:
                wt += area * dy
            elif cy > y_center:
                wb += area * dy

        x_balance = wl - wr
        y_balance = wt - wb

        # Return the distance from perfect balance (0, 0) as penalty
        return sqrt(x_balance**2 + y_balance**2)
