import re

from app.documents.extractors.base_extractor import BaseExtractor
from app.documents.schemas.invoice_schema import InvoiceSchema


class InvoiceExtractor(BaseExtractor):

    def extract(self, text: str):

        invoice_pattern = r"INV[-/]?\d+"

        amount_pattern = r"\d+\.\d{2}"

        invoice_match = re.search(invoice_pattern, text)

        amount_match = re.search(amount_pattern, text)

        return InvoiceSchema(
            invoice_number=invoice_match.group() if invoice_match else None,
            total_amount=amount_match.group() if amount_match else None
        )
