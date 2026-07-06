from typing import Optional

from playwright.sync_api import Browser, Page, Playwright, sync_playwright

from constants import MIN_FONT_SIZE_PX
from logger import get_new_logger
from ui.canvas_context import CanvasContext

logger = get_new_logger("ui.text_measure")


class TextMeasure:
    """
    Singleton class that uses Playwright to measure the dimensions of text with a given font family and size.
    Caches sizes (relative to canvas dimensions) for font family, font size and content in order to avoid
    redundant measurements and max fitting font size for each of them.
    """

    _instance: Optional["TextMeasure"] = None  # Singleton instance
    _pw: Playwright
    _browser: Browser
    _page: Page
    _canvas_w_px: float
    _canvas_h_px: float

    # Dict of (text, font_name, font_size) to (width, height)
    _size_cache: dict[tuple[str, str, int], tuple[float, float]]
    # Dict of (text, font_name) to max fitting font size
    _max_fitting_cache: dict[tuple[str, str], int]

    def __init__(self):
        # Playwright setup
        self._pw = sync_playwright().start()
        self._browser = self._pw.chromium.launch()
        self._page = self._browser.new_page()
        # Caches
        self._size_cache = {}
        self._max_fitting_cache = {}
        # Placeholder canvas dimension
        self._canvas_w_px = -1
        self._canvas_h_px = -1
        # Set canvas dimensions in px
        self._update_canvas_dim()

    @classmethod
    def get_instance(cls) -> "TextMeasure":
        """
        Returns singleton instance of TextMeasure.
        On call will check if canvas dimensions have changed (see CanvasContext) and update if necessary (see _update_canvas_dim)
        :return: Singleton TextMeasure instance
        """
        if cls._instance is None:
            cls._instance = TextMeasure()

        cls._instance._update_canvas_dim()
        return cls._instance

    def _update_canvas_dim(self):
        """
        Get new canvas dimensions (denominated in px) and if they differ from the current dimensions, update them and clear caches
        as the current cached dimensions would be invalid (see clear_cache)
        """
        new_width, new_height = CanvasContext.get_instance().get_wh()
        if self._canvas_w_px != new_width or self._canvas_h_px != new_height:
            logger.debug(
                f"Canvas dim changed from ({self._canvas_w_px}, {self._canvas_h_px}) to ({new_width}, {new_height}). Clearing caches..."
            )
            self.clear_cache()
        self._canvas_w_px = new_width
        self._canvas_h_px = new_height

    def get_dim(
        self,
        text: str,
        font_family: str,
        font_size: int,
    ) -> tuple[float, float]:
        """
        Returns the normalized width and height of the text with the given font family and size.
        1. Check cache first
        2. If not in cache, set page content to a paragraph with the specified font
        :param text: The text to measure
        :param font_family: The font family to use for measurement
        :param font_size: The font size to use for measurement
        :return: A tuple of (width, height) in normalized canvas units
        """
        key = (text, font_family, font_size)
        if key in self._size_cache:
            return self._size_cache[key]

        # Set page content to paragraph with specified font and text
        self._page.set_content(
            f"""<p id="text" style="position: absolute; 
            font-family: {font_family}; 
            font-size: {font_size}px; 
            white-space: nowrap; 
            visibility: hidden;">
            {text}</p>"""
        )
        bbox = self._page.locator("#text").bounding_box()
        if bbox is None:
            raise ValueError(
                f"Bounding box is None for {text = }, {font_family = }, {font_size = }."
            )

        width_px = bbox["width"]
        height_px = bbox["height"]

        # Convert to canvas units
        width = width_px / self._canvas_w_px
        height = height_px / self._canvas_h_px

        self._size_cache[key] = (width, height)

        return width, height

    def clear_cache(self):
        self._size_cache.clear()
        self._max_fitting_cache.clear()

    def precache_font_sizes(self, text: str, font_family: str):
        """
        Will start to probe the dimensions starting at MIN_FONT_SIZE_PX and keep increasing the font size until the dimensions are larger
        than 1 in either width or height.
        :param text: The text to measure
        :param font_family: The font family to use for measurement
        """
        current_font_size = MIN_FONT_SIZE_PX
        while True:
            dim = self.get_dim(text, font_family, current_font_size)
            if dim[0] > 1 or dim[1] > 1:
                break
            current_font_size += 1
        self._max_fitting_cache[(text, font_family)] = current_font_size - 1
        logger.debug(
            f"Precached font sizes up to {current_font_size - 1} for text '{text}' and font family '{font_family}'"
        )

    def max_fitting_font_size(self, text: str, font_family: str) -> int:
        """
        Returns the maximum fitting font size for the given text and font family that fits within the canvas dimensions.
        :param text: The text to measure
        :param font_family: The font family to use for measurement
        :return: The maximum fitting font size in pixels
        """
        key = (text, font_family)
        if key not in self._max_fitting_cache:
            raise ValueError(
                f"Max fitting font size for {key = } not precached. Call precache_font_sizes first."
            )
        return self._max_fitting_cache[key]

    @classmethod
    def close(cls):
        """
        Close and stop the playwright instance and reset the singleton instance.
        """
        if cls._instance is not None:
            cls._instance._page.close()
            cls._instance._browser.close()
            cls._instance._pw.stop()
            cls._instance = None
