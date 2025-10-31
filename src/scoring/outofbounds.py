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
            bbox = element.bbox
            top_left = self._distance_to_canvas(bbox.x, bbox.y)
            top_right = self._distance_to_canvas(bbox.x + bbox.width, bbox.y)
            bottom_left = self._distance_to_canvas(bbox.x, bbox.y + bbox.height)
            bottom_right = self._distance_to_canvas(
                bbox.x + bbox.width, bbox.y + bbox.height
            )
            # TODO: Maybe average instead of sum?
            if (
                top_left == 0
                and top_right == 0
                and bottom_left == 0
                and bottom_right == 0
            ):
                score += 10
            else:
                score -= top_left + top_right + bottom_left + bottom_right
        return score

