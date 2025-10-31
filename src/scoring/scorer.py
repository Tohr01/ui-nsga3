from abc import ABC, abstractmethod

from genetic.ui import UserInterface


class Scorer(ABC):
    @abstractmethod
    def score(self, ui: UserInterface) -> float:
        raise NotImplementedError("Score method must be implemented by subclasses.")
