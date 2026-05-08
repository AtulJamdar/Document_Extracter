class OCRException(Exception):

    def __init__(self, message: str):
        self.message = message


class ClassificationException(Exception):

    def __init__(self, message: str):
        self.message = message


class ExtractionException(Exception):

    def __init__(self, message: str):
        self.message = message


class ValidationException(Exception):

    def __init__(self, message: str):
        self.message = message