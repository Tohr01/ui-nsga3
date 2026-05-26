from scoring.scorer import Scorer


class MinTouchTargetSizeScorer(Scorer):
    """
    Scores a container based on how many of its elements are below the minimum, recommended
    touch target size of 44px x 44px.

    Source: https://www.w3.org/WAI/WCAG21/Understanding/target-size
    Latest accessed: 2026-05-02
    """

    def score(self, container) -> float:
        penalty = 0.0
        count_target_elements = 0
        for element in container.elements:
            if element.config.is_touch_target:
                w, h = element.size.get_wh()
                # Convert rel units to px
                w_px = w * container.width_px
                h_px = h * container.height_px

                w_penalty = max(0.0, 44 - w_px) / container.width_px
                h_penalty = max(0.0, 44 - h_px) / container.height_px
                penalty += w_penalty + h_penalty
                count_target_elements += 1

        return penalty / count_target_elements if count_target_elements > 0 else 0.0
