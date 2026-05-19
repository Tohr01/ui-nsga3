from scoring.scorer import Scorer
from ui.container import Container


class ScreenSpaceUtitizationScorer(Scorer):
    """
    This scorer penalizes unused screen space (width*height)
    It calculates the total area covered by the elements and returns a penality based on
    the unused area (1 - min(1.0, area_covered)) to ensure the score is between 0 and 1.

    Based on source: https://www.nngroup.com/articles/utilize-available-screen-space/
    Latest accessed: 2026-05-13
    """

    def score(self, container: Container) -> float:
        area_covered = sum(
            w * h for element in container.elements for w, h in [element.size.get_wh()]
        )

        return 1 - min(1.0, area_covered)
