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
