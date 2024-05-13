import logging.config
import os
from typing import Any, List

import yaml
from fastapi import FastAPI, UploadFile, Request
from fastapi.openapi.utils import get_openapi
from starlette.responses import FileResponse

from teal.core import create_json_err_response_from_exception
from teal.libreoffice import LibreOfficeAdapter
from teal.model import TextExtract, TableExtract
from teal.pdf import PdfDataExtractor, PdfAConverter

app = FastAPI()

log_conf_file = "log_conf.yaml"
if 'TEAL_LOG_CONF' in os.environ:
    log_conf_file = os.environ['TEAL_LOG_CONF']

print(f"using TEAL_LOG_CONF {log_conf_file}")

with open(log_conf_file, 'rt') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

# get root logger
logger = logging.getLogger("teal.api")


@app.exception_handler(Exception)
async def unicorn_exception_handler(request: Request, ex: Exception):
    return create_json_err_response_from_exception(ex)


@app.post("/pdf/text", response_model=List[TextExtract], tags=['pdf'])
async def extract_text_from_pdf(
        file: UploadFile,
) -> Any:
    logger.debug(f"extract text from pdf file='{file.filename}'")
    pdf = PdfDataExtractor()
    return pdf.extract_text(data=await file.read(), filename=file.filename)


@app.post("/pdf/ocr", response_model=List[TextExtract], tags=['pdf'])
async def extract_text_with_ocr_from_pdf(
        file: UploadFile,
) -> Any:
    logger.debug(f"extract text with ocr from pdf file='{file.filename}'")
    pdf = PdfDataExtractor()
    return pdf.extract_text_with_ocr(data=await file.read(), filename=file.filename)


@app.post("/pdf/table", response_model=List[TableExtract], tags=['pdf'])
async def extract_table_from_pdf(
        file: UploadFile,
) -> Any:
    logger.debug(f"extract table from pdf file='{file.filename}'")
    pdf = PdfDataExtractor()
    return pdf.extract_table(data=await file.read(), filename=file.filename)


@app.post("/convert/pdf", response_class=FileResponse, tags=['convert'])
async def convert_pdf_to_pdfa_with_ocr(
        file: UploadFile,
) -> Any:
    logger.debug(f"extract table from pdf file='{file.filename}'")
    pdf = PdfAConverter()
    return pdf.convert_pdf(data=await file.read(), filename=file.filename)


@app.post("/convert/libreoffice", response_class=FileResponse, tags=['convert'])
async def convert_libreoffice_docs_to_pdf(
        file: UploadFile,
) -> Any:
    logger.debug(f"libreoffice convert file='{file.filename}' to pdf")
    libreoffice = LibreOfficeAdapter()
    return libreoffice.convert_to_pdf(data=await file.read(), filename=file.filename)


def custom_openapi():
    tags_metadata = [
        {
            "name": "pdf",
            "description": "Extract text, OCR or tables from PDFs",
        },
        {
            "name": "convert",
            "description": "Convert documents to PDF or PDFs to PDF/A.",
        },
    ]

    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="teal",
        version="0.1.0",
        summary="A convenient REST API for working with PDF's",
        description="**teal** aims to provide a user-friendly API for working with PDFs which can be easily integrated in an existing workflow. ",
        routes=app.routes,
        tags=tags_metadata
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
