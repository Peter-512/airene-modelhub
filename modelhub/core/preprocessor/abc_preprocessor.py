from abc import ABC, abstractmethod


class AbstractPreprocessor(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def preprocess(self, data: str) -> None:
        pass
