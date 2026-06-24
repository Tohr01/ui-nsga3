from enum import Enum
from math import sqrt

import numpy as np

from scoring.scorer import Scorer
from ui.container import Container


class SymmetryMode(Enum):
    VERTICAL = 0
    HORIZONTAL = 1
    RADIAL = 2


class SymmetryScorer(Scorer):
    """
    Scores a Container based on the symmetry of its elements.

    References:
    -----------
    [1] D. Ngo, A. Samsudin und R. Abdullah,
        „Aesthetic Measures for Assessing Graphic Screens“,
        Journal Of Information Science And Engineering,
        Bd. 16, Nr. 1, S. 97–116, Jan. 2000,
        doi: 10.6688/jise.2000.16.1.4.
    """

    mode: SymmetryMode
    MAX_PENALTY = sqrt(0.5**2 + 0.5**2 + 1.0**2 + 1.0**2)

    def __init__(self, mode: SymmetryMode = SymmetryMode.VERTICAL):
        self.mode = mode

    def score(self, container: Container) -> float:
        num_elements = len(container.elements)
        if num_elements == 0:
            return 0.0

        x_center = 0.5
        y_center = 0.5
        g_ul = [0.0, 0.0, 0.0, 0.0]
        g_ur = [0.0, 0.0, 0.0, 0.0]
        g_ll = [0.0, 0.0, 0.0, 0.0]
        g_lr = [0.0, 0.0, 0.0, 0.0]

        for element in container.elements:
            pos = element.position
            size = element.size
            x_center_elem = pos.x + size.width / 2
            y_center_elem = pos.y + size.height / 2
            x_diff = abs(x_center_elem - x_center)
            y_diff = abs(y_center_elem - y_center)

            is_right = x_center_elem >= x_center
            is_bottom = y_center_elem >= y_center

            selected_g: list[float] = []
            if not is_right and not is_bottom:
                selected_g = g_ul
            elif is_right and not is_bottom:
                selected_g = g_ur
            elif not is_right and is_bottom:
                selected_g = g_ll
            else:
                selected_g = g_lr

            selected_g[0] += x_diff
            selected_g[1] += y_diff
            selected_g[2] += size.width
            selected_g[3] += size.height

        g_ul = np.array(g_ul, dtype=float)
        g_ur = np.array(g_ur, dtype=float)
        g_ll = np.array(g_ll, dtype=float)
        g_lr = np.array(g_lr, dtype=float)

        penalty = 0.0
        if self.mode == SymmetryMode.VERTICAL:
            g_ul_ur_diff = g_ul - g_ur
            g_ll_lr_diff = g_ll - g_lr
            penalty = float(np.linalg.norm(g_ul_ur_diff) + np.linalg.norm(g_ll_lr_diff))
        elif self.mode == SymmetryMode.HORIZONTAL:
            g_ul_ll_diff = g_ul - g_ll
            g_ur_lr_diff = g_ur - g_lr
            penalty = float(np.linalg.norm(g_ul_ll_diff) + np.linalg.norm(g_ur_lr_diff))
        elif self.mode == SymmetryMode.RADIAL:
            g_ul_lr_diff = g_ul - g_lr
            g_ur_ll_diff = g_ur - g_ll
            penalty = float(np.linalg.norm(g_ul_lr_diff) + np.linalg.norm(g_ur_ll_diff))
        else:
            raise ValueError(f"Unknown symmetry mode: {self.mode}")

        penalty_norm_elements = penalty / num_elements
        return penalty_norm_elements / self.MAX_PENALTY
