from math import sqrt

from scoring.scorer import Scorer
from ui.container import Container


class HeaderScorer(Scorer):
    def score(self, container: Container) -> float:
        penalty = 0
        for element in container.elements:
            if element.label == "Header":
                x, y = element.position.get_xy()
                w, h = element.size.get_wh()
                w_penalty = 1 - w
                # Penalize if header is not at the top left of the container and doesnt span the full width
                x_penalty = x
                # FIX: This is a hardcoded optimal height
                h_penalty = 0.1 - h
                y_penalty = y
                penalty += sqrt(
                    x_penalty**2 + w_penalty**2 + h_penalty**2 + y_penalty**2
                )

        return penalty
