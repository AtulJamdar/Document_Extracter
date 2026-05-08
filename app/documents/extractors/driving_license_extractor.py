import re

from app.documents.extractors.base_extractor import BaseExtractor
from app.documents.schemas.driving_license_schema import DrivingLicenseSchema


class DrivingLicenseExtractor(BaseExtractor):

    def extract(self, text: str):

        dl_pattern = r"[A-Z]{2}\d{2}\s\d{11}"

        dl_match = re.search(dl_pattern, text)

        return DrivingLicenseSchema(
            license_number=dl_match.group() if dl_match else None
        )
