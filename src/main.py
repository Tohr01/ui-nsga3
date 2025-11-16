from datetime import time
from typing import Type
from PIL import Image
import numpy as np
import random
import csv
from time import time

from constants import (
    FITNESS_MAX_STAGNATION_GENERATIONS,
    MAX_GENERATIONS,
    MAX_RELATIONAL_HEIGHT,
    MAX_RELATIONAL_WIDTH,
    OUTPUT_DIR,
    POPULATION_SIZE,
)
from genetic.ui import UserInterface
from scoring.balance import BalanceScorer
from scoring.equilibrium import EquilibriumScorer
from scoring.outofbounds import OutOfBoundsScorer
from scoring.padding import PaddingScorer
from scoring.symmetry import SymmetryMode, SymmetryScorer
from ui.components.image import ScaledImageView
from ui.element import UIElement
from ui.renderer import HTMLRenderer
from util import init_output_dir

print(MAX_RELATIONAL_HEIGHT, MAX_RELATIONAL_WIDTH)

random.seed(42)
np.random.seed(42)

init_output_dir()

# Structure of elements that should be optimized
# tuples of class and a initializer dict
interface_base_structure: list[tuple[Type[UIElement], dict]] = [
    (ScaledImageView, {"image": Image.open("images/mountains.jpg")}),
    (ScaledImageView, {"image": Image.open("images/mountains.jpg")}),
    (ScaledImageView, {"image": Image.open("images/mountains.jpg")}),
    (ScaledImageView, {"image": Image.open("images/mountains.jpg")}),
]

# Scorers to evaluate UIs with weights
scorers = [
    (OutOfBoundsScorer(), 1),
    (BalanceScorer(), 1),
    (PaddingScorer(), 1),
    (EquilibriumScorer(), 1),
    (SymmetryScorer(mode=SymmetryMode.HORIZONTAL), 1),
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

score_details: list[dict] = []
top_fitness_scores: list[float] = []
best_fitness = float("-inf")
stag_count = 0

for generation_num in range(1, MAX_GENERATIONS + 1):
    print(f"Processing generation {generation_num}...")
    # Score all UIs
    fitness_scores = []
    gen_min_fitness = float("inf")
    gen_max_fitness = float("-inf")
    for i, ui in enumerate(population):
        total_score = 0

        score_detail: dict[str, int | float] = {
            "# Generation": generation_num,
            "# Individual": i + 1,
        }

        for scorer, weight in scorers:
            score = scorer.score(ui) * weight
            score_detail[scorer.__class__.__name__] = score
            total_score += score
        score_detail["Score"] = total_score
        score_details.append(score_detail)
        gen_min_fitness = min(gen_min_fitness, total_score)
        gen_max_fitness = max(gen_max_fitness, total_score)

        fitness_scores.append(total_score)
        HTMLRenderer.ui_to_html(
            ui=ui,
            output_path=OUTPUT_DIR / f"generation-{generation_num}/{i + 1}.html",
        )
    fitness_scores = np.array(fitness_scores, dtype=float)
    top_fitness_scores.append(gen_max_fitness)

    if gen_max_fitness <= best_fitness:
        stag_count += 1
    else:
        best_fitness = gen_max_fitness
        print(
            f"New best fitness: {best_fitness} in generation {generation_num} on individual {np.argmax(fitness_scores) + 1}"
        )
        stag_count = 0

    # Break if we have hit a fitness plateau
    if stag_count == FITNESS_MAX_STAGNATION_GENERATIONS:
        print(
            f"Fitness has not improved in {FITNESS_MAX_STAGNATION_GENERATIONS} generations. Stopping."
        )
        break

    # Shift scores to be non-negative
    if gen_min_fitness < 0:
        fitness_scores += abs(gen_min_fitness)

    # TODO: Maybe perform an elite selection

    # Create new population
    new_population = []
    # Perform roulette wheel selection
    fitness_sum = fitness_scores.sum()
    if fitness_sum == 0:
        probs = np.ones_like(fitness_scores) / len(fitness_scores)
    else:
        probs = fitness_scores / fitness_sum

    while len(new_population) < POPULATION_SIZE:
        # Select the best UIs
        parents = np.random.choice(population, size=2, p=probs)

        child = UserInterface.crossover_and_mutate(
            parents[0], parents[1], MUTATION_RATE
        )
        new_population.append(child)
    population = new_population

print(f"Best fitness score: {best_fitness}")

# Write scores csv
with open(OUTPUT_DIR / "scores.csv", mode="w", newline="") as score_file:
    fieldnames = [
        "# Generation",
        "# Individual",
        "Score",
        *[scorer.__class__.__name__ for scorer, _weight in scorers],
    ]
    writer = csv.DictWriter(score_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(score_details)
