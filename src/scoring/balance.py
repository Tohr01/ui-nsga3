from constants import CANVAS_ASPECT_RATIO_X, CANVAS_ASPECT_RATIO_Y
from genetic.ui import UserInterface
from scoring.scorer import Scorer
from math import sqrt


class BalanceScorer(Scorer):
    """
    Scores a UI based on the balance of its elements.
    Forumla is based on the paper "Aesthetic Measures for Assessing Graphic Screens"
    See 3.1 https://www.researchgate.net/publication/220587460_Aesthetic_Measures_for_Assessing_Graphic_Screens
    """

    def score(self, ui: UserInterface) -> float:
        x_center = 0.5
        y_center = 0.5
        wl, wr, wt, wb = 0, 0, 0, 0
        for element in ui.elements:
            pos = element.position
            size = element.size

            area = size.visual_area()
            cx = pos.x + size.width / 2
            cy = pos.y + size.height / 2

            dx = abs(x_center - cx) * CANVAS_ASPECT_RATIO_X
            dy = abs(y_center - cy) * CANVAS_ASPECT_RATIO_Y
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
