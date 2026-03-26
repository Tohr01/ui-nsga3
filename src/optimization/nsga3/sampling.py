import numpy as np
from pymoo.util.misc import Sampling

from ui.container import Container
from ui.structure import BlueprintContainer


class ContainerSampling(Sampling):
    container_width_px: float
    container_height_px: float
    blueprint: BlueprintContainer

    def __init__(
        self,
        container_width_px: float,
        container_height_px: float,
        blueprint: BlueprintContainer,
    ) -> None:
        super().__init__()
        self.container_width_px = container_width_px
        self.container_height_px = container_height_px
        self.blueprint = blueprint

    def _do(self, problem, n_samples, *args, random_state=None, **kwargs):
        population = []
        for _ in range(n_samples):
            container = self.blueprint.get_new_container(
                self.container_width_px, self.container_height_px
            )
            population.append(container)

        return np.array(population, dtype=Container).reshape(n_samples, 1)
