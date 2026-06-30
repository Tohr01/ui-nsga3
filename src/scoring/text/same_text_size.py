from warnings import deprecated

from scoring.scorer import Scorer
from ui.components.text import Text
from ui.container import Container


@deprecated("Deprecated in favor of GoldenRatioTextSizeScorer")
class SameTextSizeScorer(Scorer):
    """
    Penalizes containers that have text elements of varying sizes.
    Will only penalize text elements of the same type (e.g. paragraphs)
    See TextType in ui/enums.py for more details on text types.

    Source: https://b13.com/blog/designing-with-type-a-guide-to-ui-font-size-guidelines
    Latest accessed: 2026-05-06
    """

    def score(self, container: Container) -> float:
        text_elements = [e for e in container.elements if isinstance(e, Text)]
        text_type_to_font_sizes = {}
        for element in text_elements:
            text_type = element.config.text_type
            if text_type not in text_type_to_font_sizes:
                text_type_to_font_sizes[text_type] = []
            text_type_to_font_sizes[text_type].append(element.font_size)

        penalty = 0
        for font_sizes in text_type_to_font_sizes.values():
            if len(font_sizes) > 1:
                max_size = max(font_sizes)
                if max_size > 0:
                    penalty += (max_size - min(font_sizes)) / max_size

        return (
            penalty / len(text_type_to_font_sizes)
            if len(text_type_to_font_sizes) > 0
            else 0.0
        )
