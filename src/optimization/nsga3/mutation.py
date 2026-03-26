import copy

from pymoo.core.mutation import Mutation


class ContainerMutation(Mutation):
    mutation_rate: float

    def __init__(self, mutation_rate: float = 0.1) -> None:
        super().__init__()
        self.mutation_rate = mutation_rate

    def _do(self, problem, X, *args, random_state=None, **kwargs):
        for i in range(len(X)):
            # Deepcopy before inplace modification
            container = X[i, 0]
            copied_container = copy.deepcopy(container)
            # PERF: Maybe optimize by making mutation return a new container instead of mutating in place
            copied_container.mutate(self.mutation_rate)
            # Set mutated container back to X
            X[i, 0] = copied_container

        return X
