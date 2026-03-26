from typing import Type

import numpy as np
from pymoo.core.problem import Problem

from scoring.padding import PaddingScorer
from scoring.scorer import Scorer


class ContainerProblem(Problem):
    scorers: list[tuple[Scorer, float]]
    # TODO: Outsource
    padding_scorer: PaddingScorer

    def __init__(self, scorers: list[tuple[Type[Scorer], float]]):
        # We set n_var to 1 because we will pass a single Container object as the variable to optimize
        super().__init__(n_var=1, n_obj=len(scorers), n_ieq_constr=1)
        # Init scorers
        self.scorers = [(scorer(), weight) for scorer, weight in scorers]
        self.padding_scorer = PaddingScorer()

    def _evaluate(self, x, out, *args, **kwargs):
        objectives = []
        constraints = []
        for container in x[:, 0]:
            scores = [
                scorer.score(container) * weight for scorer, weight in self.scorers
            ]
            objectives.append(scores)

            padding_score = self.padding_scorer.score(container)
            constraints.append([padding_score])

        out["F"] = np.array(objectives, dtype=float)
        out["G"] = np.array(constraints, dtype=float)
