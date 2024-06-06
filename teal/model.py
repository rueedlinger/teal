from enum import Enum
from typing import List

from pydantic import BaseModel


class HealthCheck(BaseModel):

    status: str = "OK"


class TextExtract(BaseModel):
    page: int
    text: str


class TableExtract(BaseModel):
    page: int
    index: int = 0
    table: List[dict]


class HttpRemoteRepository(BaseModel):
    url: str
    params: dict


class PdfAReport(BaseModel):
    profile: str
    statement: str
    compliant: bool
    details: dict = {}


class PdfMetaDataReport(BaseModel):
    fileName: str
    fileSize: int
    pdfVersion: str
    pdfaClaim: str | None
    pages: int
    docInfo: dict = {}
    xmp: dict = {}


class OcrPdfAProfile(str, Enum):
    PDFA_1B = "pdfa-1b"
    PDFA_2B = "pdfa-2b"
    PDFA_3B = "pdfa-3b"

    def to_ocrmypdf_profile(self):
        return self.value[:-1]


class LibreOfficePdfProfile(str, Enum):
    PDFA_1B = "pdfa-1b"
    PDFA_2B = "pdfa-2b"
    PDFA_3B = "pdfa-3b"
    PDF_15 = "pdf-1.5"
    PDF_16 = "pdf-1.6"
    PDF17 = "pdf-1.7"

    def to_libreoffice_pdf_version(self):
        if "pdfa-" in self.value:
            return self.value.replace("pdfa-", "").replace("a", "").replace("b", "")
        elif "pdf-" in self.value:
            return self.value.replace("pdf-", "").replace(".", "")
        else:
            return "0"


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
