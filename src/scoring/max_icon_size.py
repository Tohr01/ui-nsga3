from scoring.scorer import Scorer
from ui.components.aspect_image import AspectImage
from ui.components.cover_image import CoverImage
from ui.container import Container


class MaxIconSizeScorer(Scorer):
    """
    Penalizes a container based on how many of its icon are above a certain size threshold.
    The size threshold is set at >= 48px based on the design guidelines from michelin

    "Don’t use icons over 32px, icons are meant to be used at small scale, starting 48px icons will start to look like pictograms"

    Source: https://designsystem.michelin.com/icons/brand/icons-pictograms/icons/usage
    Latest accessed: 2026-05-20
    """

    def score(self, container: Container) -> float:
        penalty = 0.0
        count_icon_elements = 0
        for element in container.elements:
            if not (
                isinstance(element, AspectImage) or isinstance(element, CoverImage)
            ):
                continue

            w, h = element.size.get_wh()
            # Convert rel units to px
            w_px = w * container.width_px
            h_px = h * container.height_px

            w_penalty = max(0.0, w_px - 48) / container.width_px
            h_penalty = max(0.0, h_px - 48) / container.height_px
            penalty += w_penalty + h_penalty
            count_icon_elements += 1

        return penalty / count_icon_elements if count_icon_elements > 0 else 0.0
