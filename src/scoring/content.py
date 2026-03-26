from math import sqrt

from scoring.scorer import Scorer
from ui.container import Container


class ContentScorer(Scorer):
    def score(self, container: Container) -> float:
        penalty = 0

        header = next((e for e in container.elements if e.label == "Header"), None)
        footer = next((e for e in container.elements if e.label == "Footer"), None)
        content = next((e for e in container.elements if e.label == "Content"), None)

        if content is None:
            return 0.0

        x, y = content.position.get_xy()
        w, h = content.size.get_wh()

        # X: Start at left should start at left edge; span full width
        x_penalty = x * container.width_aspect_ratio
        w_penalty = (1.0 - w) * container.width_aspect_ratio

        # Y: should start directly below header (if header exists)
        y_optimal = header.size.height if header else 0.0

        # Height: should fill space between header bottom and footer top (if footer exists)
        footer_h = footer.size.height if footer else 0.0
        h_optimal = 1.0 - y_optimal - footer_h
        y_penalty = abs(y - y_optimal) * container.height_aspect_ratio
        h_penalty = abs(h - h_optimal) * container.height_aspect_ratio

        penalty += sqrt(x_penalty**2 + y_penalty**2 + w_penalty**2 + h_penalty**2)
        return penalty
