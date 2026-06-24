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

    # Max contribution per element is 0.5 (given no element is out of bounds)
    # area * |x_center - cx| <= 0.5
    # If all elements are e.g. in wl x_balance = num_elements * 0.5 (same for y)
    MAX_PENALTY = sqrt(2) / 2

    def score(self, container: Container) -> float:
        num_elements = len(container.elements)
        if num_elements == 0:
            return 0.0

        # NOTE: WHEN CHANGING THIS CHANGE NORMALIZATION
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
        raw_penalty = sqrt(x_balance**2 + y_balance**2) / num_elements
        return raw_penalty / self.MAX_PENALTY
