from math import sqrt

from scoring.scorer import Scorer
from ui.container import Container


class FooterScorer(Scorer):
    def score(self, container: Container) -> float:
        penalty = 0
        for element in container.elements:
            if element.label == "Footer":
                x, y = element.position.get_xy()
                w, h = element.size.get_wh()
                # Penalize if footer is not at the of bottom the container and doesnt span the full width
                w_penalty = 1 - w
                x_penalty = x
                # FIX: This is a hardcoded optimal height
                h_penalty = 0.1 - h
                y_optimal = 1 - h
                y_penalty = abs(y - y_optimal)
                penalty += sqrt(
                    x_penalty**2 + w_penalty**2 + h_penalty**2 + y_penalty**2
                )

        return penalty
