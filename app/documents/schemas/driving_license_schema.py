from pydantic import BaseModel
from typing import Optional


class DrivingLicenseSchema(BaseModel):

    license_number: Optional[str] = None
