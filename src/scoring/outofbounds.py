from genetic.ui import UserInterface
from scoring.scorer import Scorer
from math import sqrt


class OutOfBoundsScorer(Scorer):
    def _distance_to_canvas(self, x: float, y: float) -> float:
        dx = max(-x, 0, x - 1)
        dy = max(-y, 0, y - 1)
        return sqrt(dx**2 + dy**2)

    def score(self, ui: UserInterface) -> float:
        score = 0
        for element in ui.elements:
            pos = element.position
            size = element.size
            top_left = self._distance_to_canvas(pos.x, pos.y)
            top_right = self._distance_to_canvas(pos.x + size.width, pos.y)
            bottom_left = self._distance_to_canvas(pos.x, pos.y + size.height)
            bottom_right = self._distance_to_canvas(
                pos.x + size.width, pos.y + size.height
            )
            # TODO: Reward if some edge is on the canvas?
            score -= top_left + top_right + bottom_left + bottom_right
        return score
