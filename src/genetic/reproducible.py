from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T", bound="Reproducible")


class Reproducible(ABC, Generic[T]):
    @staticmethod
    @abstractmethod
    def crossover(i1: T, i2: T) -> T:
        """
        Crossover two individuals to produce a new individual.
        :param i1: First individual
        :param i2: Second individual
        :return: New individual
        """
        raise NotImplementedError("crossover method must be implemented by subclass.")

    @abstractmethod
    def mutate(self, mutation_rate: float):
        """
        Mutate the individual. (Normally by changing its attributes)
        :param mutation_rate: The mutation rate to be used during mutation
        """
        raise NotImplementedError("mutate method must be implemented by subclass.")

    @staticmethod
    def crossover_and_mutate(i1: T, i2: T, mutation_rate: float) -> T:
        """
        Perform crossover and mutation on two individuals to produce a new individual.
        :param i1: First individual
        :param i2: Second individual
        :param mutation_rate: The mutation rate to be used during mutation
        :return: New individual after crossover and mutation
        """
        assert type(i1) is type(i2), (
            "Individuals must be of the same type for crossover."
        )
        offspring = type(i1).crossover(i1, i2)
        offspring.mutate(mutation_rate)
        return offspring

    @abstractmethod
    def mutatable_gene_count(self) -> int:
        """
        Return the number of mutatable genes in the individual.
        :return: Number of mutatable genes
        """
        raise NotImplementedError(
            "mutatable_gene_count method must be implemented by subclass."
        )
