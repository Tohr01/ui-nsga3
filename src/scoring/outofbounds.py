from math import sqrt

from scoring.scorer import Scorer
from ui.container import Container


# TODO: Remove this file as it is currently not used (we use a repair function)
class OutOfBoundsScorer(Scorer):
    def score(self, container: Container) -> float:
        def _distance_to_canvas(x: float, y: float) -> float:
            dx = max(-x, 0, x - 1) * container.width_aspect_ratio
            dy = max(-y, 0, y - 1) * container.height_aspect_ratio
            return sqrt(dx**2 + dy**2)

        penalty = 0
        for element in container.elements:
            x, y = element.position.get_xy()
            w, h = element.size.get_wh()
            top_left = _distance_to_canvas(x, y)
            top_right = _distance_to_canvas(x + w, y)
            bottom_left = _distance_to_canvas(x, y + h)
            bottom_right = _distance_to_canvas(x + w, y + h)
            # TODO: Reward if some edge is on the canvas?
            penalty += top_left + top_right + bottom_left + bottom_right
        return penalty
