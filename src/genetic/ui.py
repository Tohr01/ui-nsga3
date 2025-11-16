from genetic.reproducible import Reproducible
from ui.element import UIElement


class UserInterface(Reproducible):
    elements: list[UIElement] = []

    def __init__(self, elements: list[UIElement]):
        self.elements = elements

    @staticmethod
    def random() -> "UserInterface":
        raise NotImplementedError("random is not supported on the UserInterface class.")

    @staticmethod
    def crossover(i1: "UserInterface", i2: "UserInterface") -> "UserInterface":
        new_elements: list[UIElement] = []
        for element1, element2 in zip(i1.elements, i2.elements):
            assert type(element1) is type(element2), (
                "Crossover can only be performed on UserInnterfaces with the same elements."
            )
            new_elements.append(type(element1).crossover(element1, element2))
        return UserInterface(new_elements)

    def mutate(self, mutation_rate: float):
        for element in self.elements:
            element.mutate(mutation_rate)

    def mutatable_gene_count(self) -> int:
        return sum(element.mutatable_gene_count() for element in self.elements)
