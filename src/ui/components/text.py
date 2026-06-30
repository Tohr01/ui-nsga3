from dataclasses import dataclass
from typing import Optional

from numpy import clip
from numpy.random import randint

from constants import DEFAULT_FONT_FAMILY, MIN_FONT_SIZE_PX
from genetic.attributes.position import Position
from genetic.attributes.size import Size
from genetic.mutation import normal_distribution_mutate
from genetic.recombination import intermediate_recombination
from rendering.util import styles_dict_to_str
from ui.element import TextlikeElement, TextlikeElementConfig
from ui.text_measure import TextMeasure


@dataclass
class TextConfig(TextlikeElementConfig):
    enable_font_size_crossover: bool = True
    enable_font_size_mutation: bool = True


class Text(TextlikeElement):
    """
    The Text UIElement represents a text element with a specific font size and family.
    Position and font size can be mutated and crossed over. The size will be inferred
    from the text content, font size and family.

    NOTE: Requires preprocessing by the TextMeasure class
    NOTE: When inputting a multiline text make sure to use <br> for line breaks
    """

    config: TextConfig  # type: ignore[override]

    def __init__(
        self,
        text: str,
        font_size: Optional[int] = None,
        font_family: str = DEFAULT_FONT_FAMILY,
        label: Optional[str] = None,
        position: Optional[Position] = None,
        config: TextConfig = TextConfig(),
    ):
        self.text = text
        self.font_family = font_family
        self._max_font_size = TextMeasure.get_instance().max_fitting_font_size(
            text, self.font_family
        )
        self.font_size = (
            font_size
            if font_size is not None
            else randint(MIN_FONT_SIZE_PX, self._max_font_size + 1)
        )
        # Get size in rel units based on font size and text dimensions
        width, height = TextMeasure.get_instance().get_dim(
            text, self.font_family, self.font_size
        )
        self._max_font_size = TextMeasure.get_instance().max_fitting_font_size(
            text, self.font_family
        )
        size = Size(width, height)
        super().__init__(label=label, position=position, size=size, config=config)

    @staticmethod
    def crossover(i1: "Text", i2: "Text") -> "Text":
        # Crossover position
        new_position = (
            Position.crossover(i1.position, i2.position)
            if i1.config.enable_position_crossover
            else i1.position
        )
        # Crossover font size
        new_font_size = (
            int(intermediate_recombination(i1.font_size, i2.font_size))
            if i1.config.enable_font_size_crossover
            else i1.font_size
        )
        new_font_size = clip(
            new_font_size,
            MIN_FONT_SIZE_PX,
            i1._max_font_size,
        )
        return Text(
            text=i1.text,
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
            # Update size based on new font size
            self.size.width, self.size.height = TextMeasure.get_instance().get_dim(
                self.text, self.font_family, self.font_size
            )

    def clamp_to_canvas(self):
        """
        Shrink font size until the text fits within the canvas bounds,
        then clamp the position to be inside the canvas bounds.
        """
        # NOTE: Currently the shrinking is not really needed as the TextMeasure class
        # provides a max fitting font size that is used during mutation and crossover
        # For robustness we keep the shrinking mechanism
        while (
            self.size.width > 1 or self.size.height > 1
        ) and self.font_size > MIN_FONT_SIZE_PX:
            self.font_size -= 1
            self.size.width, self.size.height = TextMeasure.get_instance().get_dim(
                self.text, self.font_family, self.font_size
            )

        # Now the text fits within the canvas bounds, we just need to clamp the position
        self.position.x = clip(self.position.x, 0, 1 - self.size.width)
        self.position.y = clip(self.position.y, 0, 1 - self.size.height)

    def to_html_element(self) -> str:
        styles = {
            "position": "absolute",
            "margin": "0",
            "padding": "0",
            "font-family": self.font_family,
            "font-size": f"{self.font_size}px",
            "left": f"{self.position.x * 100}%",
            "top": f"{self.position.y * 100}%",
            "white-space": "nowrap",
        }
        return f'<p style="{styles_dict_to_str(styles)}">{self.text}</p>'
