import re

from app.documents.extractors.base_extractor import BaseExtractor
from app.documents.schemas.passport_schema import PassportSchema


class PassportExtractor(BaseExtractor):

    def extract(self, text: str):

        passport_pattern = r"[A-Z][0-9]{7}"

        passport_match = re.search(passport_pattern, text)

        nationality = None

        if "india" in text.lower():
            nationality = "Indian"

        return PassportSchema(
            passport_number=passport_match.group() if passport_match else None,
            nationality=nationality
        )
