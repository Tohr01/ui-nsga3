import numpy as np
import random
from pathlib import Path

from constants import POPULATION_SIZE
from genetic.ui import UserInterface
from scoring.outofbounds import OutOfBoundsScorer
from ui.components.box import Box
from ui.renderer import HTMLRenderer


random.seed(42)
np.random.seed(42)

# Structure of elements that should be optimized
interface_base_structure = [Box]

# Scorers to evaluate UIs
scorers = [OutOfBoundsScorer()]

# Initialize population
initial_population = []
for i in range(POPULATION_SIZE):
    elements = [component.random() for component in interface_base_structure]
    ui = UserInterface(elements)
    initial_population.append(ui)

MUTATION_RATE = 0.01

population = initial_population
for generation_num in range(1, 501):
    print(f"Processing generation {generation_num}...")
    # Score all UIs
    fitness_scores = []
    for i, ui in enumerate(population):
        total_score = 0

        for scorer in scorers:
            total_score += scorer.score(ui)
        fitness_scores.append(total_score)
        HTMLRenderer.ui_to_html(
            ui=ui,
            output_path=Path(f"output/generation-{generation_num}/{i}.html"),
        )
    fitness_scores = np.array(fitness_scores, dtype=float)
    print(len([s for s in fitness_scores if s > 0]))
    # Shift scores to be non-negative
    min_score = np.min(fitness_scores)
    if min_score < 0:
        fitness_scores += abs(min_score)

    # TODO: Maybe perform an elite selection

    # Create new population
    new_population = []
    while len(new_population) < POPULATION_SIZE:
        # Perform roulette wheel selection
        fitness_sum = fitness_scores.sum()
        if fitness_sum == 0:
            probabilities = np.ones_like(fitness_scores) / len(fitness_scores)
        else:
            probabilities = fitness_scores / fitness_sum

        # Select the best UIs
        parents = np.random.choice(population, size=2, p=probabilities)
        child = UserInterface.crossover_and_mutate(
            parents[0], parents[1], MUTATION_RATE
        )
        new_population.append(child)
    population = new_population
