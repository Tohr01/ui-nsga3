from scoring.scorer import Scorer
from ui.components.aspect_image import AspectImage
from ui.components.cover_image import CoverImage
from ui.container import Container


class MaxIconSizeScorer(Scorer):
    """
    Penalizes a container based on how many of its icon are above a certain size threshold.
    The size threshold is set at >= 48px based on the design guidelines from Michelin

    "Don’t use icons over 32px, icons are meant to be used at small scale, starting 48px icons will start to look like pictograms"

    References:
    -----------
    [1] Michelin, “Icons - Usage,” Michelin Design System.
        https://designsystem.michelin.com/icons/brand/icons-pictograms/icons/usage
        (accessed May 20, 2026).
    """

    MAX_TOUCH_TARGET_WIDTH_PX = 48
    MAX_TOUCH_TARGET_HEIGHT_PX = 48

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

            # Guard against small canvas using the max
            # NOTE: If the canvas is smaller the penalty can get big
            # TODO: Maybe change this behavior
            max_canvas_w_overhead = max(
                1.0, container.width_px - self.MAX_TOUCH_TARGET_WIDTH_PX
            )
            max_canvas_h_overhead = max(
                1.0, container.height_px - self.MAX_TOUCH_TARGET_HEIGHT_PX
            )

            w_penalty = (
                max(0.0, w_px - self.MAX_TOUCH_TARGET_WIDTH_PX) / max_canvas_w_overhead
            )
            h_penalty = (
                max(0.0, h_px - self.MAX_TOUCH_TARGET_HEIGHT_PX) / max_canvas_h_overhead
            )
            penalty += (w_penalty + h_penalty) / 2
            count_icon_elements += 1

        return penalty / count_icon_elements if count_icon_elements > 0 else 0.0
