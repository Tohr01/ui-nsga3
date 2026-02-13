from typing import Type
import json
import numpy as np
import random
from collections import defaultdict

from constants import (
    FITNESS_MAX_STAGNATION_GENERATIONS,
    MAX_GENERATIONS,
    OUTPUT_DIR,
    POPULATION_SIZE,
)
from genetic.ui import UserInterface
from scoring.balance import BalanceScorer
from scoring.equilibrium import EquilibriumScorer
from scoring.outofbounds import OutOfBoundsScorer
from scoring.padding import PaddingScorer
from scoring.symmetry import SymmetryMode, SymmetryScorer
from ui.components.box import Box
from ui.element import UIElement
from ui.renderer import HTMLRenderer
from util import init_output_dir

random.seed(42)
np.random.seed(42)

init_output_dir()

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


MUTATION_RATE = 0.1

population: list[UserInterface] = []

# Initialize population
for i in range(POPULATION_SIZE):
    elements = [
        component(**init_params) for component, init_params in interface_base_structure
    ]
    ui = UserInterface(elements)
    population.append(ui)

# Generation number -> individual number -> scorer name & total score -> score
fitness_details: dict[int, dict[int, dict[str, float]]] = {}
best_fitness = float("inf")
stag_count = 0

for generation_num in range(1, MAX_GENERATIONS + 1):
    print(f"Processing generation {generation_num}...")
    # Score all UIs; lower is better
    fitness_scores = []
    gen_best_fitness = float("inf")
    gen_worst_fitness = float("-inf")

    fitness_details[generation_num] = defaultdict(dict)

    for i, ui in enumerate(population):
        total_score = 0
        for scorer, weight in scorers:
            score = scorer.score(ui) * weight
            fitness_details[generation_num][i+1][scorer.__class__.__name__] = score
            total_score += score

        fitness_details[generation_num][i+1]["total_score"] = total_score
        gen_best_fitness = min(gen_best_fitness, total_score)
        gen_worst_fitness = max(gen_worst_fitness, total_score)

        fitness_scores.append(total_score)
        HTMLRenderer.ui_to_html(
            ui=ui,
            output_path=OUTPUT_DIR / f"generation-{generation_num}/{i + 1}.html",
        )
    fitness_scores = np.array(fitness_scores, dtype=float)

    if gen_best_fitness >= best_fitness:
        # We have not seen improvement in fitness, increase stagnation count
        stag_count += 1
    else:
        best_fitness = gen_best_fitness
        print(
            f"New best fitness: {best_fitness} in generation {generation_num} on individual {np.argmin(fitness_scores) + 1}"
        )
        # We have seen improvement in fitness, reset stagnation count
        stag_count = 0

    # Break if we have hit a fitness plateau
    if stag_count == FITNESS_MAX_STAGNATION_GENERATIONS:
        print(
            f"Fitness has not improved in {FITNESS_MAX_STAGNATION_GENERATIONS} generations. Stopping..."
        )
        break

    # TODO: Maybe perform an elite selection and tournament selection

    inverted_fitness_scores = np.array(fitness_scores, dtype=float)

    # Shift scores to be non-negative
    if gen_best_fitness < 0:
        inverted_fitness_scores -= gen_best_fitness

    # Invert fitness scores for roulette wheel selection (now higher is better)
    inverted_fitness_scores = inverted_fitness_scores.max() - fitness_scores

    # Perform roulette wheel selection
    inverted_fitness_sum = inverted_fitness_scores.sum()
    print(fitness_scores, inverted_fitness_scores)
    if inverted_fitness_sum == 0:
        probs = np.ones_like(inverted_fitness_scores) / len(inverted_fitness_scores)
    else:
        probs = inverted_fitness_scores / inverted_fitness_scores

    # Create new population
    new_population = []

    while len(new_population) < POPULATION_SIZE:
        # Select the best UIs
        parents = np.random.choice(population, size=2, p=probs)

        child = UserInterface.crossover_and_mutate(
            parents[0], parents[1], MUTATION_RATE
        )
        new_population.append(child)
    population = new_population

print(f"Best fitness score: {best_fitness}")

# Write json with fitness fitness_details
with open(OUTPUT_DIR / "fitness_details.json", "w") as f:
    json.dump(fitness_details, f, indent=4)
