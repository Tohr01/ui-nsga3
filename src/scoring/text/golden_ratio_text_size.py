from scipy.constants import golden_ratio

from scoring.scorer import Scorer
from ui.container import Container
from ui.element import TextlikeElement
from ui.enums import TextType


# FIX: Docstring to make consistent with other scorers source credit
class GoldenRatioTextSizeScorer(Scorer):
    """
    Let φ be the golden ratio.
    Let X be the base body (paragraph) font size.

    The scorer will try to optimize towards the following font sizes
    HEADER = φ^2 * X
    SUBHEADER = φ^1 * X
    PARAGRAPH = φ^0 * X
    FOOTNOTE = φ^(-1) * X
    OTHER = φ^0 * X

    Sources (Latest accessed: 2026-06-16):
    • https://cieden.com/book/sub-atomic/typography/different-type-scale-types
    • https://www.nngroup.com/articles/golden-ratio-ui-design/
    """

    # NOTE: Change when changing the text type in enums.py
    _role_exponents = {
        TextType.HEADER: 2,
        TextType.SUBHEADER: 1,
        TextType.PARAGRAPH: 0,
        TextType.FOOTNOTE: -1,
        TextType.OTHER: 0,
    }

    def score(self, container: Container) -> float:
        text_elements = [
            e for e in container.elements if isinstance(e, TextlikeElement)
        ]

        if len(text_elements) == 0:
            return 0.0

        # Find reference size X
        text_groups: dict[TextType, list[TextlikeElement]] = {}
        for element in text_elements:
            text_type = element.config.text_type
            if text_type not in text_groups:
                text_groups[text_type] = []
            text_groups[text_type].append(element)

        # Estimate paragraph font size from every element
        est_x_sizes = []
        for text_type, elements in text_groups.items():
            exponent = self._role_exponents.get(
                text_type, 0
            )  # Default to 0 (paragraph size)
            for element in elements:
                paragraph_size = element.font_size / (golden_ratio**exponent)
                est_x_sizes.append(paragraph_size)

        avg_x_size = sum(est_x_sizes) / len(est_x_sizes)

        penalty = 0.0
        for text_type, elements in text_groups.items():
            exponent = self._role_exponents.get(
                text_type, 0
            )  # Default to 0 (paragraph size)
            target = (golden_ratio**exponent) * avg_x_size
            for element in elements:
                penalty += abs(element.font_size - target) / avg_x_size

        return penalty / len(text_elements)
