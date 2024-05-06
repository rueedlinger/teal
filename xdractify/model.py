from enum import Enum
from typing import Union, List, Annotated

from fastapi import File
from pydantic import BaseModel


class DataEncoding(str, Enum):
    base64 = "base64"
    text = "text"


class PdfAction(str, Enum):
    table = "table"
    text = "text"


class Document(BaseModel):
    name: str
    data: str
    encoding: DataEncoding


class PdfDocument(Document):
    actions: List[PdfAction]
