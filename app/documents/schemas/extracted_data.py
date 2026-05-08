from pydantic import BaseModel
from typing import Dict, Any


class ExtractedData(BaseModel):

    fields: Dict[str, Any]
