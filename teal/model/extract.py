from enum import Enum
from typing import List

from pydantic import BaseModel


class TextExtractMode(str, Enum):
    RAW = "raw"
    OCR = "ocr"


class TableExtractMode(str, Enum):
    LATTICE = "lattice"
    STREAM = "stream"


class TextExtract(BaseModel):
    page: int
    text: str
    mode: TextExtractMode | None = None


class TableExtract(BaseModel):
    page: int
    index: int = 0
    table: List[dict]
    mode: TableExtractMode | None = None


class PdfMetaDataReport(BaseModel):
    fileName: str
    fileSize: int
    pdfVersion: str
    pdfaClaim: str | None
    pages: int
    docInfo: dict | None = {}
    xmp: dict | None = {}
