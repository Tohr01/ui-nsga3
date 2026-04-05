from pymoo.core.repair import Repair


class CanvasBoundsRepair(Repair):
    def _do(self, problem, X, **kwargs):
        for container in X[:, 0]:
            for element in container.elements:
                element.clamp_to_canvas()
        return X
