from math import sqrt

from scoring.scorer import Scorer
from ui.container import Container


class BalanceScorer(Scorer):
    """
    Scores a Container based on the balance of its elements.

    References:
    -----------
    [1] D. Ngo, A. Samsudin und R. Abdullah,
        „Aesthetic Measures for Assessing Graphic Screens“,
        Journal Of Information Science And Engineering,
        Bd. 16, Nr. 1, S. 97–116, Jan. 2000,
        doi: 10.6688/jise.2000.16.1.4.
    """

    def score(self, container: Container) -> float:
        x_center = 0.5
        y_center = 0.5
        wl, wr, wt, wb = 0, 0, 0, 0
        for element in container.elements:
            pos = element.position
            size = element.size

            area = size.area()
            cx = pos.x + size.width / 2
            cy = pos.y + size.height / 2

            dx = abs(x_center - cx)
            dy = abs(y_center - cy)
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
        num_elements = len(container.elements)
        return (
            sqrt(x_balance**2 + y_balance**2) / num_elements
            if num_elements != 0
            else 0.0
        )
