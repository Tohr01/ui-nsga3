from math import sqrt

from scoring.scorer import Scorer


class MinTouchTargetSizeScorer(Scorer):
    """
    Scores a container based on how many of its elements are below the minimum, recommended
    touch target size of 44px x 44px.

    Source: https://www.w3.org/WAI/WCAG21/Understanding/target-size
    Latest accessed: 2026-05-02
    """

    def score(self, container) -> float:
        penalty = 0
        for element in container.elements:
            if element.config.is_touch_target:
                # Convert rel units to pixels.
                w, h = element.size.get_wh()
                w_px = w * container.width_px
                h_px = h * container.height_px
                w_penality = (
                    max(0, 44 - w_px) / container.width_px
                ) * container.width_aspect_ratio
                h_penality = (
                    max(0, 44 - h_px) / container.height_px
                ) * container.height_aspect_ratio
                penalty += sqrt(w_penality**2 + h_penality**2)

        return penalty
