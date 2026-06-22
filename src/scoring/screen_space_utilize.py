from scoring.scorer import Scorer
from ui.container import Container


class ScreenSpaceUtilizationScorer(Scorer):
    """
    This scorer penalizes unused screen space
    It calculates the total area covered by the elements and returns a penality based on
    the unused area (1 - min(1.0, area_covered)) to ensure the score is between 0 and 1.

    References:
    -----------
    [1] J. Nielsen, “Utilize available screen space,” Nielsen Norman Group,
        Apr. 19, 2018. https://www.nngroup.com/articles/utilize-available-screen-space/
        (accessed May 13, 2026).
    """

    def score(self, container: Container) -> float:
        # NOTE: Because our iequality contraints flags overlapping elements as illegal we
        # sum the area of each element. Otherwise we would have to calculate the overlapping
        # union area
        area_covered = sum(
            w * h for element in container.elements for w, h in [element.size.get_wh()]
        )

        return 1 - min(1.0, area_covered)
