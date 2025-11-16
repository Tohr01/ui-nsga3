from enum import Enum
from genetic.ui import UserInterface
from scoring.scorer import Scorer
import numpy as np
from math import sqrt


class SymmetryMode(Enum):
    VERTICAL = 0
    HORIZONTAL = 1
    RADIAL = 2


class SymmetryScorer(Scorer):
    """
    Scores a UI based on the symmetry of its elements.
    Forumla is based on the paper "Aesthetic Measures for Assessing Graphic Screens"
    See 3.3 https://www.researchgate.net/publication/220587460_Aesthetic_Measures_for_Assessing_Graphic_Screens
    """

    mode: SymmetryMode

    def __init__(self, mode: SymmetryMode = SymmetryMode.VERTICAL):
        self.mode = mode

    def score(self, ui: UserInterface) -> float:
        x_c = 0.5
        y_c = 0.5
        g_ul = [0.0, 0.0, 0.0, 0.0]
        g_ur = [0.0, 0.0, 0.0, 0.0]
        g_ll = [0.0, 0.0, 0.0, 0.0]
        g_lr = [0.0, 0.0, 0.0, 0.0]

        for element in ui.elements:
            pos = element.position
            size = element.size
            x_center_elem = pos.x + size.width / 2
            y_center_elem = pos.y + size.height / 2
            x_diff = abs(x_center_elem - x_c)
            y_diff = abs(y_center_elem - y_c)
            selected_g: list[float] = []
            if x_center_elem < x_c and y_center_elem < y_c:
                selected_g = g_ul
            elif x_center_elem > x_c and y_center_elem < y_c:
                selected_g = g_ur
            elif x_center_elem < x_c and y_center_elem > y_c:
                selected_g = g_ll
            elif x_center_elem > x_c and y_center_elem > y_c:
                selected_g = g_lr
            else:
                # NOTE:: Element is exactly in the center on at least on axis, skip it
                continue
            selected_g[0] = selected_g[0] + x_diff
            selected_g[1] += y_diff
            selected_g[2] += size.width
            selected_g[3] += size.height

        g_ul = np.array(g_ul, dtype=float)
        g_ur = np.array(g_ur, dtype=float)
        g_ll = np.array(g_ll, dtype=float)
        g_lr = np.array(g_lr, dtype=float)

        if self.mode == SymmetryMode.VERTICAL:
            g_ul_ur_diff = g_ul - g_ur
            g_ll_lr_diff = g_ll - g_lr
            return (
                -float(np.linalg.norm(g_ul_ur_diff) + np.linalg.norm(g_ll_lr_diff)) / 2
            )
        elif self.mode == SymmetryMode.HORIZONTAL:
            g_ul_ll_diff = g_ul - g_ll
            g_ur_lr_diff = g_ur - g_lr
            return (
                -float(np.linalg.norm(g_ul_ll_diff) + np.linalg.norm(g_ur_lr_diff)) / 2
            )
        elif self.mode == SymmetryMode.RADIAL:
            g_ul_lr_diff = g_ul - g_lr
            g_ur_ll_diff = g_ur - g_ll
            return (
                -float(np.linalg.norm(g_ul_lr_diff) + np.linalg.norm(g_ur_ll_diff)) / 2
            )
        else:
            raise ValueError(f"Unknown symmetry mode: {self.mode}")
