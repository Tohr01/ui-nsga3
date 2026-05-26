from scoring.scorer import Scorer
from ui.container import Container


class MinSizeScorer(Scorer):
    # NOTE: Non inclusive
    MIN_WIDTH: float
    MIN_HEIGHT: float

    def __init__(self, min_width: float = 0.0, min_height: float = 0.0):
        self.MIN_WIDTH = min_width
        self.MIN_HEIGHT = min_height

    def score(self, container: Container) -> float:
        penalty = 0.0
        illegal_element_count = 0
        for element in container.elements:
            w, h = element.size.get_wh()
            if w > self.MIN_WIDTH and h > self.MIN_HEIGHT:
                continue
            element_penalty = 0.0

            illegal_axis_count = 0
            if w <= self.MIN_WIDTH:
                element_penalty += max(0.0, 1.0 - w)
                illegal_axis_count += 1
            if h <= self.MIN_HEIGHT:
                element_penalty += max(0.0, 1.0 - h)
                illegal_axis_count += 1

            penalty += element_penalty / illegal_axis_count
            illegal_element_count += 1

        return penalty / illegal_element_count if illegal_element_count > 0 else 0.0
