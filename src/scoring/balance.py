from constants import CANVAS_HEIGHT_NORM, CANVAS_WIDTH_NORM
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
        x_center = CANVAS_WIDTH_NORM / 2
        y_center = CANVAS_HEIGHT_NORM / 2
        wl, wr, wt, wb = 0, 0, 0, 0
        for element in ui.elements:
            pos = element.position
            size = element.size
            area = size.area()
            x_center_elem = pos.x + size.width / 2
            y_center_elem = pos.y + size.height / 2
            if x_center_elem < x_center:
                wl += area * (x_center - x_center_elem)
            elif x_center_elem > x_center:
                wr += area * (x_center_elem - x_center)

            if y_center_elem < y_center:
                wt += area * (y_center - y_center_elem)
            elif y_center_elem > y_center:
                wb += area * (y_center_elem - y_center)

        x_balance = wl - wr
        y_balance = wt - wb
        return -sqrt(x_balance**2 + y_balance**2)
