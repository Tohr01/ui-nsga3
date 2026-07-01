from typing import Optional

from logger import get_new_logger

logger = get_new_logger("ui.canvas_context")


class CanvasContext:
    """
    Singleton class holding current context about the canvas dimensions and aspect ratio.
    """

    _instance: Optional["CanvasContext"] = None  # Singleton instance

    width_px: float
    height_px: float
    aspect_ratio: float

    @classmethod
    def get_instance(cls) -> "CanvasContext":
        if CanvasContext._instance is None:
            CanvasContext._instance = CanvasContext()
        return CanvasContext._instance

    def set_canvas_dim(self, width_px: float, height_px: float):
        logger.debug(f"Setting canvas dimensions to ({width_px}px, {height_px}px)")
        self.width_px = width_px
        self.height_px = height_px
        self.aspect_ratio = width_px / height_px

    def get_wh(self) -> tuple[float, float]:
        if not hasattr(self, "width_px") or not hasattr(self, "height_px"):
            raise ValueError("Canvas dimensions not set. Call set_canvas_dim() first.")
        return self.width_px, self.height_px
