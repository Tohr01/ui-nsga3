from pymoo.core.repair import Repair


class CanvasBoundsRepair(Repair):
    def _do(self, problem, X, **kwargs):
        for container in X[:, 0]:
            for element in container.elements:
                # Clamp size
                element.size.width = max(0, min(element.size.width, 1))
                element.size.height = max(0, min(element.size.height, 1))
                # Clamp position
                element.position.x = max(
                    0, min(element.position.x, 1 - element.size.width)
                )
                element.position.y = max(
                    0, min(element.position.y, 1 - element.size.height)
                )
        return X
