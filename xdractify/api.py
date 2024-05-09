import binascii
import logging.config
from typing import Any, List

import yaml
from fastapi import FastAPI, UploadFile, Request
from starlette.responses import JSONResponse

from xdractify.model import (
    TextExtract,
    TableExtract,
)
from xdractify.pdf import PdfTextExtractor, PdfTableExtractor, PdfOcrExtractor

app = FastAPI()
with open('log_conf.yaml', 'rt') as f:
    config = yaml.safe_load(f.read())
logging.config.dictConfig(config)

# get root logger
logger = logging.getLogger("xdractify.api")


@app.exception_handler(binascii.Error)
async def unicorn_exception_handler(request: Request, ex: binascii.Error):
    return JSONResponse(
        status_code=400,
        content={"message": f"bas46 error, {ex}"},
    )


@app.exception_handler(Exception)
async def unicorn_exception_handler(request: Request, ex: binascii.Error):
    return JSONResponse(
        status_code=500,
        content={"message": f"{ex}"},
    )


@app.post("/pdf/text", response_model=List[TextExtract])
async def extract_text_from_pdf(
        file: UploadFile,
) -> Any:
    logger.debug(f"extract text from pdf file='{file.filename}'")
    pdf = PdfTextExtractor()
    return pdf.extract_text_pypdfium(data=await file.read())


@app.post("/pdf/ocr", response_model=List[TextExtract])
async def extract_text_with_ocr_from_pdf(
        file: UploadFile,
) -> Any:
    logger.debug(f"extract text with ocr from pdf file='{file.filename}'")
    pdf = PdfOcrExtractor()
    return pdf.extract_text(data=await file.read())


@app.post("/pdf/table", response_model=List[TableExtract])
async def extract_table_from_pdf(
        file: UploadFile,
) -> Any:
    logger.debug(f"extract table from pdf file='{file.filename}'")
    pdf = PdfTableExtractor()
    return pdf.extract_table(data=await file.read())


"""

@app.post("/base64/encode", response_model=Document)
async def encode_file_to_base64(file: UploadFile) -> Any:
    logger.debug(
        f"base64 encode: filename='{file.filename}', size='{file.size}', content_type='{file.content_type}'"
    )
    b64 = Base64()
    return b64.encode(data=await file.read(), filename=file.filename)
"""
