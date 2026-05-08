from abc import ABC, abstractmethod


class BaseLLMService(ABC):

    @abstractmethod
    def extract_fields(
        self,
        text: str,
        fields: list
    ):
        pass
