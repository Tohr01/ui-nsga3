from typing import Optional

from numpy import clip
from numpy.random import randint, uniform

from constants import DEFAULT_FONT_FAMILY, MIN_FONT_SIZE_PX
from genetic.attributes.position import Position
from genetic.attributes.size import Size
from genetic.mutation import normal_distribution_mutate
from genetic.recombination import intermediate_recombination
from rendering.util import styles_dict_to_str
from ui.canvas_context import CanvasContext
from ui.element import TextlikeElement, TextlikeElementConfig
from ui.text_measure import TextMeasure


class PaddingButtonConfig(TextlikeElementConfig):
    enable_font_size_crossover: bool = True
    enable_font_size_mutation: bool = True
    enable_padding_crossover: bool = True
    enable_padding_mutation: bool = True


class PaddingButton(TextlikeElement):
    """
    An UIElement representing a button with text and padding around it.
    The padding and font size can be mutated and crossed over.
    NOTE: Currently the button background and text color are fixed.
    """

    background_color_hex: str
    text_color_hex: str

    padding_width: float
    padding_height: float
    config: PaddingButtonConfig  # type: ignore[override]

    def __init__(
        self,
        text: str,
        background_color_hex: str,
        text_color_hex: str,
        padding_width: Optional[float] = None,
        padding_height: Optional[float] = None,
        font_size: Optional[int] = None,
        font_family: str = DEFAULT_FONT_FAMILY,
        label: Optional[str] = None,
        position: Optional[Position] = None,
        config: PaddingButtonConfig = PaddingButtonConfig(),
    ):
        self.text = text
        self.background_color_hex = background_color_hex
        self.text_color_hex = text_color_hex

        # Font settings
        self.font_family = font_family
        self._max_font_size = TextMeasure.get_instance().max_fitting_font_size(
            text, self.font_family
        )
        self.font_size = (
            font_size
            if font_size is not None
            else randint(MIN_FONT_SIZE_PX, self._max_font_size + 1)
        )
        text_width, text_height = TextMeasure.get_instance().get_dim(
            text, font_family, self.font_size
        )

        self.padding_width = (
            padding_width
            if padding_width is not None
            else uniform(0, (1 - text_width) / 2)
        )
        self.padding_height = (
            padding_height
            if padding_height is not None
            else uniform(0, (1 - text_height) / 2)
        )

        size = Size(
            width=text_width + 2 * self.padding_width,
            height=text_height + 2 * self.padding_height,
        )
        super().__init__(label=label, position=position, size=size, config=config)

    @staticmethod
    def crossover(i1: "PaddingButton", i2: "PaddingButton") -> "PaddingButton":
        # Crossover padding width
        new_padding_width = (
            intermediate_recombination(i1.padding_width, i2.padding_width)
            if i1.config.enable_padding_crossover
            else i1.padding_width
        )
        # Crossover padding height
        new_padding_height = (
            intermediate_recombination(i1.padding_height, i2.padding_height)
            if i1.config.enable_padding_crossover
            else i1.padding_height
        )
        # Crossover position
        new_position = (
            Position.crossover(i1.position, i2.position)
            if i1.config.enable_position_crossover
            else i1.position
        )
        # Crossover new font size
        new_font_size = (
            int(intermediate_recombination(i1.font_size, i2.font_size))
            if i1.config.enable_font_size_crossover
            else i1.font_size
        )
        new_font_size = clip(new_font_size, MIN_FONT_SIZE_PX, i1._max_font_size)
        return PaddingButton(
            text=i1.text,
            background_color_hex=i1.background_color_hex,
            text_color_hex=i1.text_color_hex,
            padding_width=new_padding_width,
            padding_height=new_padding_height,
            font_size=new_font_size,
            font_family=i1.font_family,
            label=i1.label,
            position=new_position,
            config=i1.config,
        )

    def mutate(self, mutation_rate: float):
        # Mutate position
        if self.config.enable_position_mutation:
            self.position.mutate(mutation_rate)

        # Mutate font size
        if self.config.enable_font_size_mutation:
            self.font_size = clip(
                int(
                    normal_distribution_mutate(
                        value=self.font_size,
                        mutation_rate=mutation_rate,
                        i_min=MIN_FONT_SIZE_PX,
                        i_max=self._max_font_size,
                    )
                ),
                MIN_FONT_SIZE_PX,
                self._max_font_size,
            )

        text_width, text_height = TextMeasure.get_instance().get_dim(
            self.text, self.font_family, self.font_size
        )

        # Mutate padding width and height
        if self.config.enable_padding_mutation:
            self.padding_width = normal_distribution_mutate(
                value=self.padding_width,
                mutation_rate=mutation_rate,
                i_min=0,
                i_max=(1 - text_width) / 2,
            )
            self.padding_height = normal_distribution_mutate(
                value=self.padding_height,
                mutation_rate=mutation_rate,
                i_min=0,
                i_max=(1 - text_height) / 2,
            )

        # Update size
        self.size = Size(
            width=text_width + 2 * self.padding_width,
            height=text_height + 2 * self.padding_height,
        )

    def clamp_to_canvas(self):
        """
        Makes sure that the button fits within the canvas.
        Will do the following things in order:
        1. Shrink padding if necessary
        2. Shrink font size if necessary
        3. Clamp position to fit within canvas
        """
        # Make sure the size is not larger than the canvas
        # First shrink padding if necessary
        # Second shrink font size if necessary
        text_width, text_height = TextMeasure.get_instance().get_dim(
            self.text, self.font_family, self.font_size
        )
        max_padding_width = (1 - text_width) / 2
        max_padding_height = (1 - text_height) / 2
        self.padding_width = clip(self.padding_width, 0, max_padding_width)
        self.padding_height = clip(self.padding_height, 0, max_padding_height)
        while text_width > 1 or text_height > 1:
            self.font_size -= 1
            text_width, text_height = TextMeasure.get_instance().get_dim(
                self.text, self.font_family, self.font_size
            )
            self.size.width = text_width + 2 * self.padding_width
            self.size.height = text_height + 2 * self.padding_height

        # If text shrinking did not ran
        self.size.width = text_width + 2 * self.padding_width
        self.size.height = text_height + 2 * self.padding_height

        # Now the text + padding should fit within the canvas
        self.position.x = clip(self.position.x, 0, 1 - self.size.width)
        self.position.y = clip(self.position.y, 0, 1 - self.size.height)

    def to_html_element(self) -> str:
        cc = CanvasContext.get_instance()
        styles = {
            "position": "absolute",
            "margin": "0",
            "padding-left": f"{self.padding_width * cc.width_px}px",
            "padding-right": f"{self.padding_width * cc.width_px}px",
            "padding-top": f"{self.padding_height * cc.height_px}px",
            "padding-bottom": f"{self.padding_height * cc.height_px}px",
            "font-family": self.font_family,
            "font-size": f"{self.font_size}px",
            "left": f"{self.position.x * 100}%",
            "top": f"{self.position.y * 100}%",
            "background-color": self.background_color_hex,
            "color": self.text_color_hex,
            "white-space": "nowrap",
            "border-width": "0px",
        }
        return f'<button style="{styles_dict_to_str(styles)}">{self.text}</button>'
