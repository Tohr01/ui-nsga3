import numpy as np
from pymoo.core.problem import Problem

from scoring.scorer import Scorer


class ContainerProblem(Problem):
    scorers: list[tuple[Scorer, float]]
    constraints: list[Scorer]

    def __init__(
        self,
        scorers: list[tuple[Scorer, float]],
        constraints: list[Scorer],
    ):
        # We set n_var to 1 because we will pass a single Container object as the variable to optimize
        super().__init__(n_var=1, n_obj=len(scorers), n_ieq_constr=len(constraints))
        # Init scorers
        self.scorers = [(scorer, weight) for scorer, weight in scorers]
        self.constraints = constraints

    def _evaluate(self, x, out, *args, **kwargs):
        objectives = []
        constraints = []
        for container in x[:, 0]:
            scores = [
                scorer.score(container) * weight for scorer, weight in self.scorers
            ]
            objectives.append(scores)

            container_constraint_violations = [
                constraint.score(container) for constraint in self.constraints
            ]
            constraints.append(container_constraint_violations)
        out["F"] = np.array(objectives, dtype=float)
        out["G"] = np.array(constraints, dtype=float)
