from pydantic import BaseModel
from typing import Optional


class AadhaarSchema(BaseModel):

    name: Optional[str] = None

    dob: Optional[str] = None

    aadhaar_number: Optional[str] = None
