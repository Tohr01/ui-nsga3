from scoring.scorer import Scorer
from ui.components.singleline_text import SingleLineText
from ui.container import Container


class TargetFontSizeScorer(Scorer):
    TARGET_FONT_SIZE_PX = 60

    def score(self, container: Container) -> float:
        penalty = 0
        for element in container.elements:
            if isinstance(element, SingleLineText):
                penalty += abs(element.font_size - self.TARGET_FONT_SIZE_PX)

        return penalty
