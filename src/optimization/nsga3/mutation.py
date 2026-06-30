import copy

from pymoo.core.mutation import Mutation


class ContainerMutation(Mutation):
    """
    Mutation operator for Container objects.
    This operator applies mutation to each Container in the population with a specified mutation rate.
    In order to avoid modifying the original Container we deepcopy first before mutating.
    """

    mutation_rate: float

    def __init__(self, mutation_rate: float = 0.1) -> None:
        """
        Initialize the ContainerMutation operator with a specified mutation rate.
        :param mutation_rate: The probability of mutation for each Container.
        Will recursively mutate all genes in the Container with the same probability.
        """
        self.mutation_rate = mutation_rate
        super().__init__()

    def _do(self, problem, X, *args, random_state=None, **kwargs):
        for i in range(len(X)):
            # Deepcopy before inplace modification
            container = X[i, 0]
            # PERF: Deepcopy is expensive
            copied_container = copy.deepcopy(container)
            copied_container.mutate(self.mutation_rate)
            # Set mutated container back to X
            X[i, 0] = copied_container

        return X
