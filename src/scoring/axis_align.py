import numpy as np

from scoring.enums import Axis
from scoring.scorer import Scorer
from ui.container import Container


class AxisAlignScorer(Scorer):
    """
    Penalizes variance in the center positions of elements along a specified axis (x or y).

    References:
    -----------
    [1] Interaction Design Foundation, “What is Visual Alignment?,”
        IxDF - Interaction Design Foundation, Mar. 02, 2026.
        https://ixdf.org/literature/topics/visual-alignment#center_alignment_on_axis-18
        (accessed May 26, 2026).
    """

    align_axis: Axis

    def __init__(self, align_axis: Axis = Axis.Y):
        self.align_axis = align_axis

    def score(self, container: Container) -> float:
        penalty = 0.0
        if len(container.elements) == 0:
            return penalty

        if self.align_axis == Axis.Y:
            center_positions = np.array(
                [el.position.y + el.size.height / 2 for el in container.elements]
            )
        else:
            center_positions = np.array(
                [el.position.x + el.size.width / 2 for el in container.elements]
            )

        axis_mean = center_positions.mean()
        penalty = np.mean(np.abs(center_positions - axis_mean))

        # Max deviation is 0.5 (if all elements are either at top and bottom or left and right)
        return penalty * 2.0  # Normalize to [0, 1]
