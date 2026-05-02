from scoring.scorer import Scorer
from ui.components.singleline_text import SingleLineText
from ui.container import Container


class TargetFontSizeScorer(Scorer):
    """
    Scores a container based on how close the font size of its text elements
    are to a predifined target font size.
    """

    target_font_size_px: float

    def __init__(self, target_font_size_px: float = 16):
        """
        :param target_font_size_px: The target font size in pixels. The scorer will penalize font sizes that are further away from this target.
        """
        self.target_font_size_px = target_font_size_px

    def score(self, container: Container) -> float:
        penalty = 0
        for element in container.elements:
            if isinstance(element, SingleLineText):
                penalty += abs(element.font_size - self.target_font_size_px)

        return penalty
