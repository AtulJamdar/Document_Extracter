from abc import ABC, abstractmethod

from app.documents.schemas.classification_result import ClassificationResult


class BaseClassifier(ABC):

    @abstractmethod
    def classify(self, text: str) -> ClassificationResult:
        pass
