from enum import Enum
from typing import List

from pydantic import BaseModel


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
