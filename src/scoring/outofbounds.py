from math import sqrt
from constants import CANVAS_ASPECT_RATIO_X, CANVAS_ASPECT_RATIO_Y
from genetic.ui import UserInterface
from scoring.scorer import Scorer


class OutOfBoundsScorer(Scorer):
    def _distance_to_canvas(self, x: float, y: float) -> float:
        dx = max(-x, 0, x - 1) * CANVAS_ASPECT_RATIO_X
        dy = max(-y, 0, y - 1) * CANVAS_ASPECT_RATIO_Y
        return sqrt(dx**2 + dy**2)

    def score(self, ui: UserInterface) -> float:
        penalty = 0
        for element in ui.elements:
            x, y = element.position.get_xy()
            w, h = element.size.get_wh()
            top_left = self._distance_to_canvas(x, y)
            top_right = self._distance_to_canvas(x + w, y)
            bottom_left = self._distance_to_canvas(x, y + h)
            bottom_right = self._distance_to_canvas(
                x + w, y + h
            )
            # TODO: Reward if some edge is on the canvas?
            penalty += top_left + top_right + bottom_left + bottom_right
        return penalty

    # def score(self, ui: UserInterface) -> float:
    #     total_penalty = 0
    #     for element in ui.elements:
    #         x, y = element.position.get_xy()
    #         w, h = element.size.get_wh()
    #         penalty_left = max(0, -x)
    #         penalty_right = max(0, (x + w) - 1)
    #         penalty_top = max(0, -y)
    #         penalty_bottom = max(0, (y + h) - 1)
    #         total_penalty = penalty_left + penalty_right + penalty_top + penalty_bottom
    #
    #     return -total_penalty
