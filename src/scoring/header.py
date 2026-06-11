from math import sqrt

from scoring.scorer import Scorer
from ui.container import Container


class HeaderScorer(Scorer):
    """
    Scores the header based on its position and size.
    Examples taken from amazon.de and ebay.de
    1. Header is at the top of the container (ebay.de & amazon.de)
    2. Header spans the full width of the container (ebay.de & amazon.de)
    3. Header has a height between 98.688px (ebay.de) and 99px (amazon.de)

    Sources:
    - amazon.de (Latest accessed: 2026-06-09)
    - ebay.de (Latest accessed: 2026-06-09)

    Browser: Brave 1.91.168 at 1920x1080 webpage size
    """

    HEADER_HEIGHTS_PX = [98.688, 99]
    MIN_HEADER_HEIGHT_PX = min(HEADER_HEIGHTS_PX)
    MAX_HEADER_HEIGHT_PX = max(HEADER_HEIGHTS_PX)

    def score(self, container: Container) -> float:
        penalty = 0.0
        count_header_elements = 0
        # PERF: Caching
        min_header_height = self.MIN_HEADER_HEIGHT_PX / container.height_px
        max_header_height = self.MAX_HEADER_HEIGHT_PX / container.height_px
        for element in container.elements:
            if element.label == "Header":
                x, y = element.position.get_xy()
                w, h = element.size.get_wh()
                # Full width and height in [min_header_height; max_header_height]
                w_penalty = 1 - w
                h_penalty = max(0, min_header_height - h, h - max_header_height)
                penalty += sqrt(x**2 + y**2 + h_penalty**2 + w_penalty**2)
                count_header_elements += 1

        return penalty / count_header_elements if count_header_elements > 0 else 0.0
