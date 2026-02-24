from pathlib import Path
import numpy as np
import random

from genetic.ui import UserInterface
from scoring.scorer import Scorer

random.seed(42)
np.random.seed(42)

from typing import Type
from pymoo.algorithms.moo.nsga3 import NSGA3
from pymoo.core.problem import Problem 
from pymoo.util.ref_dirs import get_reference_directions
from pymoo.core.crossover import Crossover
from pymoo.core.mutation import Mutation
from pymoo.core.sampling import Sampling
from pymoo.optimize import minimize


from scoring.balance import BalanceScorer
from scoring.equilibrium import EquilibriumScorer
from scoring.outofbounds import OutOfBoundsScorer
from scoring.padding import PaddingScorer
from scoring.symmetry import SymmetryMode, SymmetryScorer
from ui.element import UIElement
from ui.components.box import Box
from ui.renderer import HTMLRenderer

# Structure of elements that should be optimized
# tuples of class and a initializer dict
interface_base_structure: list[tuple[Type[UIElement], dict]] = [
   (Box, {}),
   (Box, {}), 
   (Box, {}),
]

# Scorers to evaluate UIs with weights
scorers = [
   (OutOfBoundsScorer(), 1),
   (BalanceScorer(), 1),
   (PaddingScorer(), 1),
   (EquilibriumScorer(), 1),
   (SymmetryScorer(mode=SymmetryMode.HORIZONTAL), 0.5),
]

class UISampling(Sampling):
    interface_structure: list[tuple[Type[UIElement], dict]]

    def __init__(self, interface_structure: list[tuple[Type[UIElement], dict]]) -> None:
        super().__init__()
        self.interface_structure = interface_structure

    def _do(self, problem, n_samples, *args, random_state=None, **kwargs):
        population = []
        for _ in range(n_samples):
            elements = [
                component(**init_params) for component, init_params in self.interface_structure
            ]
            population.append(UserInterface(elements=elements))

        return np.array(population, dtype=UserInterface).reshape(n_samples, 1)


class UICrossover(Crossover):
    def __init__(self):
        super().__init__(n_parents=2, n_offsprings=1)

    def _do(self, problem, X, *args, **kwargs):
        _, n_matings, _ = X.shape
        
        offspring = np.empty((1, n_matings, 1), dtype=UserInterface) 
        
        for i in range(n_matings):
            p1: UserInterface = X[0, i, 0]
            p2: UserInterface = X[1, i, 0]
            child = type(p1).crossover(p1, p2)
            offspring[0, i, 0] = child

        return offspring

class UIMutation(Mutation):
    def __init__(self, mutation_rate: float) -> None:
        super().__init__()
        self.mutation_rate = mutation_rate

    def _do(self, problem, X, **kwargs):
        for ui in X[:,0]:
            ui.mutate(self.mutation_rate)

        return X

class UIProblem(Problem):

    scorers: list[tuple[Scorer, float]]
    def __init__(self, scorers: list[tuple[Scorer, float]]):
        super().__init__(n_var=1, n_obj=len(scorers))
        self.scorers = scorers

    def _evaluate(self, X, out, *args, **kwargs):
        objectives = []
        for ui in X[:, 0]:
            scores = [scorer.score(ui) * weight for scorer, weight in self.scorers]
            objectives.append(scores)

        out["F"] = np.array(objectives)


        


sampling = UISampling(interface_base_structure)


ref_dirs = get_reference_directions("energy", n_dim=len(scorers), n_points=100, seed=42)

algo = NSGA3(ref_dirs=ref_dirs, 
             sampling=UISampling(interface_base_structure), 
             crossover=UICrossover(), 
             mutation=UIMutation(mutation_rate=0.1),
             eliminate_duplicates=False)

problem = UIProblem(scorers)

optimized_uis = minimize(problem, algo, ('n_gen', 300), verbose=True)
for i, ui in enumerate(optimized_uis.X[:, 0]):
    HTMLRenderer().ui_to_html(ui, Path(f"optimized_ui_{i}.html"))

