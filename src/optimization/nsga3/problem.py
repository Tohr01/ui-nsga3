import numpy as np
from pymoo.core.problem import Problem

from scoring.scorer import Scorer


class ContainerProblem(Problem):
    scorers: list[Scorer]
    constraints: list[Scorer]

    def __init__(
        self,
        scorers: list[Scorer],
        constraints: list[Scorer],
    ):
        # We set n_var to 1 because we will pass a single Container object as the variable to optimize
        super().__init__(n_var=1, n_obj=len(scorers), n_ieq_constr=len(constraints))
        # Init scorers
        self.scorers = scorers
        self.constraints = constraints

    def _evaluate(self, x, out, *args, **kwargs):
        objectives = []
        constraints = []
        for container in x[:, 0]:
            # Eval objective functions
            scores = [scorer.score(container) for scorer in self.scorers]
            objectives.append(scores)

            # Eval ieq constraint functions
            container_constraint_violations = [
                constraint.score(container) for constraint in self.constraints
            ]
            constraints.append(container_constraint_violations)

        out["F"] = np.array(objectives, dtype=float)
        out["G"] = np.array(constraints, dtype=float)
