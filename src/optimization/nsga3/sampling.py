import numpy as np
from pymoo.util.misc import Sampling

from ui.blueprint import BlueprintContainer
from ui.container import Container


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
            container = self.get_single_container()
            population.append(container)

        return np.array(population, dtype=Container).reshape(n_samples, 1)

    def get_single_container(self) -> Container:
        return self.blueprint.get_new_container(
            self.container_width_px, self.container_height_px
        )
