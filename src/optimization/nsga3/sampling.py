import numpy as np
from pymoo.core.sampling import Sampling

from optimization.nsga3.repair import CanvasBoundsRepair
from ui.blueprint import BlueprintContainer
from ui.container import Container


class ContainerSampling(Sampling):
    """
    Sampling operator for Container objects.
    Responsible for instantiating new Container objects based on a given Blueprint and
    given canvas dimensions. Will generate a container with randomly initalized subelements.
    Every container is then repaired to ensure all elements are within the canvas bounds.
    """

    container_width_px: float
    container_height_px: float
    blueprint: BlueprintContainer
    repair: CanvasBoundsRepair

    def __init__(
        self,
        container_width_px: float,
        container_height_px: float,
        blueprint: BlueprintContainer,
        repair: CanvasBoundsRepair,
    ) -> None:
        super().__init__()
        self.container_width_px = container_width_px
        self.container_height_px = container_height_px
        self.blueprint = blueprint
        self.repair = repair

    def _do(self, problem, n_samples, *args, random_state=None, **kwargs):
        population = []
        for _ in range(n_samples):
            container = self.get_single_container()
            population.append(container)

        X = np.array(population, dtype=Container).reshape(n_samples, 1)
        # Repair population to ensure all elements are within canvas bounds
        X = self.repair._do(problem, X)
        return X

    def get_single_container(self) -> Container:
        container = self.blueprint.get_new_container(
            self.container_width_px, self.container_height_px
        )
        return container
