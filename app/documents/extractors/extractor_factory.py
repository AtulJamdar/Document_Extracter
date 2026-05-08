from app.documents.enums.document_type import DocumentType

from app.documents.extractors.aadhaar_extractor import AadhaarExtractor
from app.documents.extractors.passport_extractor import PassportExtractor
from app.documents.extractors.invoice_extractor import InvoiceExtractor
from app.documents.extractors.driving_license_extractor import DrivingLicenseExtractor


class ExtractorFactory:

    @staticmethod
    def get_extractor(document_type):

        if document_type == DocumentType.AADHAAR:
            return AadhaarExtractor()

        if document_type == DocumentType.PASSPORT:
            return PassportExtractor()

        if document_type == DocumentType.INVOICE:
            return InvoiceExtractor()

        if document_type == DocumentType.DRIVING_LICENSE:
            return DrivingLicenseExtractor()

        return None
