from typing import Optional


class CanvasContext:
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
        self.width_px = width_px
        self.height_px = height_px
        self.aspect_ratio = width_px / height_px

    def get_wh(self) -> tuple[float, float]:
        assert hasattr(self, "width_px") and hasattr(self, "height_px"), (
            "Canvas dimensions not set. Call set_canvas_dim() first."
        )
        return self.width_px, self.height_px
