import numpy as np

from scoring.scorer import Scorer
from ui.container import Container


class EqualHeightScorer(Scorer):
    """
    This scorer penalizes variance in the heights of elements within a container.

    Currently used for debugging and testing.
    """

    def score(self, container: Container) -> float:
        heights = np.array([element.size.height for element in container.elements])
        if len(heights) == 0:
            return 0.0

        penalty = float(np.var(heights))
        return min(penalty / 0.25, 1.0)  # Normalized to [0, 1]
