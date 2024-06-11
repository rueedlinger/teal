from enum import Enum
from typing import List

from pydantic import BaseModel


class ExtractMode(str, Enum):
    RAW = "raw"
    OCR = "ocr"


class TextExtract(BaseModel):
    page: int
    text: str
    mode: ExtractMode | None = None


class TableExtract(BaseModel):
    page: int
    index: int = 0
    table: List[dict]


class PdfMetaDataReport(BaseModel):
    fileName: str
    fileSize: int
    pdfVersion: str
    pdfaClaim: str | None
    pages: int
    docInfo: dict = {}
    xmp: dict = {}
