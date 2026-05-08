import re

from app.documents.extractors.base_extractor import BaseExtractor
from app.documents.schemas.aadhaar_schema import AadhaarSchema


class AadhaarExtractor(BaseExtractor):

    def extract(self, text: str):

        aadhaar_pattern = r"\d{4}\s\d{4}\s\d{4}"

        dob_pattern = r"\d{2}/\d{2}/\d{4}"

        aadhaar_match = re.search(aadhaar_pattern, text)

        dob_match = re.search(dob_pattern, text)

        lines = text.split("\n")

        possible_name = None

        for line in lines:

            cleaned = line.strip()

            if cleaned.isalpha() and len(cleaned) > 3:
                possible_name = cleaned
                break

        return AadhaarSchema(
            name=possible_name,
            dob=dob_match.group() if dob_match else None,
            aadhaar_number=aadhaar_match.group() if aadhaar_match else None
        )
