from pymoo.core.repair import Repair


class CanvasBoundsRepair(Repair):
    """
    Repair operator for Container objects.
    Ensures that all elements in the Container are within the canvas bounds.
    """

    def _do(self, problem, X, **kwargs):
        for container in X[:, 0]:
            for element in container.elements:
                element.clamp_to_canvas()
        return X
