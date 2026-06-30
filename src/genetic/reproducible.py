from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T", bound="Reproducible")


class Reproducible(ABC, Generic[T]):
    """
    Abstract base class for reproducible individuals in a genetic algorithm.
    Each class inheriting from Reproducible must implement the crossover and mutate methods.
    """

    @staticmethod
    @abstractmethod
    def crossover(i1: T, i2: T) -> T:
        """
        Crossover two individuals to produce a new individual.
        :param i1: First individual
        :param i2: Second individual
        :return: New individual
        """
        pass

    @abstractmethod
    def mutate(self, mutation_rate: float):
        """
        Mutate the individual. (Normally by changing its attributes)
        :param mutation_rate: The mutation rate to be used during mutation
        """
        pass

    @staticmethod
    def crossover_and_mutate(i1: T, i2: T, mutation_rate: float) -> T:
        """
        Perform crossover and mutation on two individuals to produce a new individual.
        :param i1: First individual
        :param i2: Second individual
        :param mutation_rate: The mutation rate to be used during mutation
        :return: New individual after crossover and mutation
        """
        if type(i1) is not type(i2):
            raise TypeError(
                f"Individuals must be of the same type for crossover. Got {type(i1)} and {type(i2)}."
            )

        offspring = type(i1).crossover(i1, i2)
        offspring.mutate(mutation_rate)
        return offspring
