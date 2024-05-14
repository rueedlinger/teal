from enum import Enum
from typing import List

from pydantic import BaseModel


class DataEncoding(str, Enum):
    base64 = "base64"
    text = "raw"


class Data(BaseModel):
    encoding: DataEncoding

    content: str


class PdfActionType(str, Enum):
    text = "text"
    table = "table"


class PdfEngine(str, Enum):
    pdfium = "pdfium"
    pypdf = "pypdf"
    tesseract = "tesseract"


class PdfModule(BaseModel):
    engine: PdfEngine
    params: dict | None = None


class Document(BaseModel):
    name: str
    data: Data


class PdfExtract(BaseModel):
    pdf: Data
    module: PdfModule


class TextExtract(BaseModel):
    page: int
    text: str


class TableExtract(BaseModel):
    page: int
    index: int = 0
    table: List[dict]


class Extracts(BaseModel):
    extracts: List[TextExtract] = []
