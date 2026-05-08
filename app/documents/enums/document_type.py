from enum import Enum


class DocumentType(str, Enum):

    AADHAAR = "aadhaar"

    PASSPORT = "passport"

    DRIVING_LICENSE = "driving_license"

    INVOICE = "invoice"

    UNKNOWN = "unknown"
