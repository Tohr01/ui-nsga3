from abc import ABC, abstractmethod

from ui.container import Container


class Scorer(ABC):
    @abstractmethod
    def score(self, container: Container) -> float:
        """
        Scores a Container based on some criteria. Higher score is worse.
        :param container: The UserInterface to score
        :return: A penalty score
        """
        pass
