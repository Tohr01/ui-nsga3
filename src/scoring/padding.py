from math import sqrt
from constants import CANVAS_ASPECT_RATIO_X, CANVAS_ASPECT_RATIO_Y
from genetic.ui import UserInterface
from scoring.scorer import Scorer
from itertools import combinations


class PaddingScorer(Scorer):
    """
    Will penalize UIs that have elements too close to each other.
    """

    PADDING_THRESHOLD = 0.15

    def score(self, ui: UserInterface) -> float:
        penalty = 0

        for e1, e2 in combinations(ui.elements, 2):
            pos1 = e1.position
            size1 = e1.size
            pos2 = e2.position
            size2 = e2.size

            # Calculate horizontal and vertical distances
            x_distance = max(
                0,
                max(pos1.x, pos2.x) - min(pos1.x + size1.width, pos2.x + size2.width),
            ) * CANVAS_ASPECT_RATIO_X
            y_distance = max(
                0,
                max(pos1.y, pos2.y) - min(pos1.y + size1.height, pos2.y + size2.height),
            ) * CANVAS_ASPECT_RATIO_Y

            distance = sqrt(x_distance**2 + y_distance**2)

            # Elements are to close
            if distance < self.PADDING_THRESHOLD:
                penalty = self.PADDING_THRESHOLD - distance

        return penalty
