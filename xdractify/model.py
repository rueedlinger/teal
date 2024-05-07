from enum import Enum
from typing import List

from pydantic import BaseModel


class DataEncoding(str, Enum):
    base64 = "base64"
    text = "text"


class Data(BaseModel):
    encoding: DataEncoding
    content: str


class PdfAction(str, Enum):
    text = "text"
    table = "table"


class PdfEngine(str, Enum):
    pdfium = "pdfium"


class Document(BaseModel):
    name: str
    data: Data


class PdfDocument(Document):
    engine: PdfEngine
    actions: List[PdfAction]


class TextExtract(BaseModel):
    page: int
    text: str


class Extracts(BaseModel):
    extracted_text: List[TextExtract]
