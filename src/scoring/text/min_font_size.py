from scoring.scorer import Scorer
from ui.container import Container
from ui.element import TextlikeElement
from ui.enums import TextType


class MinFontSizeScorer(Scorer):
    """
    Penalizes container based on the practical tips of minimum font size by the
    BFIT-Bund (Barrierefreiheit von Informationstechnik).

    They say:
    • The minimum font size for text blocks should be 22px.
    • The minimum font size for additional text (e.g. footnotes) should be 17px.

    NOTE: It is not exactly clear what a "text block" is, so we will assume it means any text element
    except footnotes in our case

    References:
    -----------
    [1] BFIT-Bund AG02 Software, “Font - Accessible design of user interface elements,”
        Überwachungsstelle Des Bundes Für Barrierefreiheit Von Informationstechnik, Mar. 24, 2025.
        https://handreichungen.bfit-bund.de/accessible-uie/schrift.html (accessed Jun. 16, 2026).
    """

    # NOTE: Change when changing the text type in enums.py
    _min_font_size_px_by_type = {
        TextType.HEADER: 22,
        TextType.SUBHEADER: 22,
        TextType.PARAGRAPH: 22,
        TextType.FOOTNOTE: 17,
        TextType.OTHER: 22,
    }

    def score(self, container: Container) -> float:
        text_elements = [
            e for e in container.elements if isinstance(e, TextlikeElement)
        ]

        if len(text_elements) == 0:
            return 0.0

        penalty = 0.0
        for element in text_elements:
            text_type = element.config.text_type
            min_size_px = self._min_font_size_px_by_type.get(
                text_type, 22
            )  # Default to 22px
            if element.font_size < min_size_px:
                penalty += (min_size_px - element.font_size) / min_size_px

        return penalty / len(text_elements)
