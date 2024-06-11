from enum import Enum

from pydantic import BaseModel


class ValidatePdfProfile(str, Enum):
    PDFA_1A = "1a"
    PDFA_1B = "1b"
    PDFA_2A = "2a"
    PDFA_2B = "2b"
    PDFA_2U = "2u"
    PDFA_3A = "3a"
    PDFA_3B = "3b"
    PDFA_3U = "3u"
    PDFA_4 = "4"
    PDFA_4e = "4e"
    PDFA_4f = "4f"
    PDFUA_1 = "ua1"
    PDFUA_2 = "ua2"


class PdfAReport(BaseModel):
    profile: str
    statement: str
    compliant: bool
    details: dict = {}
