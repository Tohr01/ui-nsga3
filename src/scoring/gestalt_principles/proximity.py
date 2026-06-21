import math
from itertools import combinations

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree

from scoring.scorer import Scorer
from ui.container import Container


class ProximityScorer(Scorer):
    """
    Scores a Container based on the proximity of its elements.
    Based on the principle of proximity in gestalt psychology. [1, 2]
    Based on the MST sum of the distance graph of the elements in each cluster. [2]

    References:
    -----------
    [1] Y. Q. Lim, “Applying white space in UI design,”
        UX Collective, Feb. 03, 2021.
        https://uxdesign.cc/whitespace-in-ui-design-44e332c8e4a (accessed May 25, 2026).
    [2] C. T. Zahn,
        “Graph-Theoretical Methods for detecting and Describing gestalt clusters,”
        IEEE Transactions on Computers,
        vol. C–20, no. 1, pp. 68–86, Jan. 1971,
        doi: 10.1109/t-c.1971.223083.
    """

    clusters: list[list[str]]

    def __init__(self, clusters: list[list[str]]) -> None:
        # TODO: Validate clusters. No duplicate label, no single elem clusters
        self.clusters = clusters

    def score(self, container: Container) -> float:
        penalty = 0.0
        elements_by_label = {el.label: el for el in container.elements}
        for cluster in self.clusters:
            elements = [elements_by_label[label] for label in cluster]
            n = len(elements)
            if n <= 1:
                continue

            # Construct triangular distance matrix for the cluster
            dist_matrix = np.zeros((n, n))
            for i, j in combinations(range(len(elements)), 2):
                d = self._bbox_distance(container, elements[i], elements[j])
                # NOTE: Matrix is symmetic as scipy minimum_spanning_tree computes the MST for
                # undirected graphs.
                dist_matrix[i, j] = (
                    d if d > 0 else 1e-9
                )  # Avoid 0 distance (invisible to scipy mst)

            mst = minimum_spanning_tree(csr_matrix(dist_matrix))
            mst_sum = mst.sum()
            # n-1 is number of edges in the mst
            penalty += mst_sum / (n - 1)

        return penalty / len(self.clusters) if len(self.clusters) else 0.0

    @staticmethod
    def _bbox_distance(container: Container, e1, e2) -> float:
        """
        Edge to edge distance between to two bounding boxes. When overlapping dist is zero.
        :param container: the container of the elements

        """
        dx = max(
            0.0,
            max(e1.position.x, e2.position.x)
            - min(e1.position.x + e1.size.width, e2.position.x + e2.size.width),
        )
        dy = max(
            0.0,
            max(e1.position.y, e2.position.y)
            - min(e1.position.y + e1.size.height, e2.position.y + e2.size.height),
        )
        return math.hypot(dx, dy)
