from scoring.scorer import Scorer


class MinTouchTargetSizeScorer(Scorer):
    """
    Scores a container based on how many of its elements are below the minimum, recommended
    touch target size of 44px x 44px.

    References:
    -----------
    [1] Accessibility Guidelines Working Group,
        “Understanding Success Criterion 2.5.5: Target Size,” Web Accessibility Initiative (WAI),
        May 11, 2026. https://www.w3.org/WAI/WCAG21/Understanding/target-size
        (accessed May 02, 2026).
    """

    MIN_TOUCH_TARGET_WIDTH_PX = 44
    MIN_TOUCH_TARGET_HEIGHT_PX = 44

    def score(self, container) -> float:
        penalty = 0.0
        count_target_elements = 0
        for element in container.elements:
            if element.config.is_touch_target:
                w, h = element.size.get_wh()
                # Convert rel units to px
                w_px = w * container.width_px
                h_px = h * container.height_px

                w_penalty = (
                    max(0.0, self.MIN_TOUCH_TARGET_WIDTH_PX - w_px)
                    / self.MIN_TOUCH_TARGET_WIDTH_PX
                )
                h_penalty = (
                    max(0.0, self.MIN_TOUCH_TARGET_HEIGHT_PX - h_px)
                    / self.MIN_TOUCH_TARGET_HEIGHT_PX
                )
                penalty += (w_penalty + h_penalty) / 2
                count_target_elements += 1

        return penalty / count_target_elements if count_target_elements > 0 else 0.0
