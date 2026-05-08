from pydantic import BaseModel
from typing import Optional


class PassportSchema(BaseModel):

    passport_number: Optional[str] = None

    nationality: Optional[str] = None
