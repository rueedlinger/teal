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
    details: dict


class PdfAProfile(str, Enum):
    PDFA1 = "pdfa-1"
    PDFA2 = "pdfa-2"
    PDFA3 = "pdfa-3"


class LibreOfficePdfProfile(str, Enum):
    PDFA1 = "pdfa-1"
    PDFA2 = "pdfa-2"
    PDFA3 = "pdfa-3"
    PDF15 = "pdf-1.5"
    PDF16 = "pdf-1.6"
    # PDF17 = "pdf-1.7"

    def to_libreoffice_pdf_version(self):
        if "pdfa-" in self.value:
            return self.value.replace("pdfa-", "")
        elif "pdf-" in self.value:
            return self.value.replace("pdf-", "").replace(".", "")
        else:
            return "0"
