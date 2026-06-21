from scipy.stats import kendalltau

from scoring.enums import Axis
from scoring.scorer import Scorer
from ui.container import Container


class ElementOrderScorer(Scorer):
    """
    Penalizes containers where the order of elements doesn't match a predefined
    order (based on either x or y pos).
    Uses a normalized Kendall Tau Distance as the penalty score (precisely 1 - normalized Kendall Tau Distance)
    """

    element_order_labels: list[str]
    order_direction: Axis

    expected_ranks: dict[str, int]

    def __init__(
        self,
        element_order_labels: list[str],
        order_direction: Axis = Axis.X,
    ) -> None:
        self.element_order_labels = element_order_labels
        self.expected_ranks = {
            label: i for i, label in enumerate(self.element_order_labels)
        }
        self.order_direction = order_direction

    def score(self, container: Container) -> float:
        element_positions = []
        for element in container.elements:
            if element.label in self.element_order_labels:
                match self.order_direction:
                    case Axis.X:
                        element_positions.append((element.label, element.position.x))
                    case Axis.Y:
                        element_positions.append((element.label, element.position.y))

        if len(element_positions) < 2:
            return 0

        # Sort by position -> current order in the container
        element_positions.sort(key=lambda t: t[1])
        current_order_labels = [label for label, _ in element_positions]

        current_rank_seq = [
            self.expected_ranks[label] for label in current_order_labels
        ]
        expected_rank_seq = list(self.expected_ranks.values())
        tau, _ = kendalltau(current_rank_seq, expected_rank_seq)

        # https://stackoverflow.com/questions/50249736/kendall-tau-distance-python-implementation-with-range-0-1
        # https://en.wikipedia.org/wiki/Kendall_tau_distance#Comparison_to_Kendall_tau_rank_correlation_coefficient
        # Normalize to [0,1]
        return 1 - (tau + 1) / 2
