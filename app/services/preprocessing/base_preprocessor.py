from abc import ABC, abstractmethod


class BasePreprocessor(ABC):

    @abstractmethod
    def preprocess(self, file_path: str):
        pass
