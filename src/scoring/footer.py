from math import sqrt

from scoring.scorer import Scorer
from ui.container import Container


class FooterScorer(Scorer):
    """
    Scores the footer based on its position and size.
    Examples taken from amazon.de and ebay.de
    1. Footer is at the bottom of the container (ebay.de & amazon.de)
    2. Footer spans the full width of the container (ebay.de & amazon.de)
    3. Footer has a height between 83px (ebay.de) and 76px (amazon.de)

    References:
    -----------
    - amazon.de (Latest accessed: 2026-06-09)
    - ebay.de (Latest accessed: 2026-06-09)

    Browser: Brave 1.91.168 at 1920x1080 webpage size
    """

    FOOTER_HEIGHTS_PX = [83, 76]
    MIN_FOOTER_HEIGHT_PX = min(FOOTER_HEIGHTS_PX)
    MAX_FOOTER_HEIGHT_PX = max(FOOTER_HEIGHTS_PX)

    def score(self, container: Container) -> float:
        penalty = 0.0
        count_footer_elements = 0
        # PERF: Caching
        min_footer_height = self.MIN_FOOTER_HEIGHT_PX / container.height_px
        max_footer_height = self.MAX_FOOTER_HEIGHT_PX / container.height_px

        MAX_PENALTY = sqrt(
            1 + 1 + max(min_footer_height, 1 - max_footer_height) ** 2 + 1
        )
        for element in container.elements:
            if element.label == "Footer":
                x, y = element.position.get_xy()
                w, h = element.size.get_wh()
                # Full width and height in [min_footer_height; max_footer_height]
                w_penalty = 1 - w
                h_penalty = max(0, min_footer_height - h, h - max_footer_height)
                y_optimal = 1 - h
                y_penalty = abs(y - y_optimal)
                penalty += (
                    sqrt(x**2 + y_penalty**2 + h_penalty**2 + w_penalty**2)
                    / MAX_PENALTY
                )
                count_footer_elements += 1

        return penalty / count_footer_elements if count_footer_elements > 0 else 0.0
