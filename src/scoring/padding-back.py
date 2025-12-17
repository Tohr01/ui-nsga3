from math import sqrt
from constants import CANVAS_HEIGHT_NORM, CANVAS_WIDTH_NORM
from genetic.ui import UserInterface
from scoring.scorer import Scorer
from itertools import combinations


class PaddingScorer(Scorer):
    """
    Will penalize UIs that have elements too close to each other.
    """

    PADDING_THRESHOLD_PCT = 0.15
    PADDING_THRESHOLD_X = CANVAS_WIDTH_NORM * PADDING_THRESHOLD_PCT
    PADDING_THRESHOLD_Y = CANVAS_HEIGHT_NORM * PADDING_THRESHOLD_PCT

    def score(self, ui: UserInterface) -> float:
        score = 0

        for e1, e2 in combinations(ui.elements, 2):
            pos1 = e1.position
            size1 = e1.size
            pos2 = e2.position
            size2 = e2.size

            # Calculate horizontal and vertical distances
            x_distance = max(
                0,
                max(pos1.x, pos2.x)
                - min(pos1.x + size1.width, pos2.x + size2.width)
                + 2 * self.PADDING_THRESHOLD_X,
            )
            y_distance = max(
                0,
                max(pos1.y, pos2.y)
                - min(pos1.y + size1.height, pos2.y + size2.height)
                + 2 * self.PADDING_THRESHOLD_Y,
            )

            # TODO: Check if performance is equally good as l2 norm
            # score -= x_distance * y_distance
            score -= sqrt(x_distance**2 + y_distance**2)

        return score
