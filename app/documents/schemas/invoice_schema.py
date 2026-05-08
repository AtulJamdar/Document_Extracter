from pydantic import BaseModel
from typing import Optional


class InvoiceSchema(BaseModel):

    invoice_number: Optional[str] = None

    total_amount: Optional[str] = None
