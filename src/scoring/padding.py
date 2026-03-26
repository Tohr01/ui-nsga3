from itertools import combinations

from scoring.scorer import Scorer
from ui.container import Container


class PaddingScorer(Scorer):
    def __init__(self, padding: float = 0.01):
        self.padding = padding

    def score(self, container: Container) -> float:
        total_overlap = 0.0
        for a, b in combinations(container.elements, 2):
            ax, ay = a.position.get_xy()
            aw, ah = a.size.get_wh()
            bx, by = b.position.get_xy()
            bw, bh = b.size.get_wh()

            # Expand each element by padding
            ax -= self.padding
            ay -= self.padding
            aw += 2 * self.padding
            ah += 2 * self.padding
            bx -= self.padding
            by -= self.padding
            bw += 2 * self.padding
            bh += 2 * self.padding

            x_overlap = max(0.0, min(ax + aw, bx + bw) - max(ax, bx))
            y_overlap = max(0.0, min(ay + ah, by + bh) - max(ay, by))
            # total overlap += area of the overlap
            total_overlap += x_overlap * y_overlap

        return total_overlap  # 0.0 = feasible, > 0.0 = infeasible
