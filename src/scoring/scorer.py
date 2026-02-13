from abc import ABC, abstractmethod

from genetic.ui import UserInterface


class Scorer(ABC):
    @abstractmethod
    def score(self, ui: UserInterface) -> float:
        """
        Scores a UI based on some criteria. Higher score is worse.
        :param ui: The UserInterface to score
        :return: A penalty score
        """
        raise NotImplementedError("Score method must be implemented by subclasses.")
