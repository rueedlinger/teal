import logging.config
import os
from typing import Any, List

import yaml
from fastapi import FastAPI, UploadFile, Request
from fastapi.openapi.utils import get_openapi
from starlette.responses import FileResponse, JSONResponse

from teal.core import create_json_err_response_from_exception, is_feature_enabled
from teal.libreoffice import LibreOfficeAdapter
from teal.model import TextExtract, TableExtract, HttpRemoteRepository
from teal.pdf import PdfDataExtractor, PdfAConverter
from teal.pdfa import PdfAValidator

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


if is_feature_enabled('TEA_FEATURE_PDF_TEXT'):
    @app.post("/pdf/text", response_model=List[TextExtract], tags=['pdf'])
    async def extract_text_from_pdf(
            file: UploadFile,
    ) -> Any:
        logger.debug(f"extract text from pdf file='{file.filename}'")
        pdf = PdfDataExtractor()
        return pdf.extract_text(data=await file.read(), filename=file.filename)

if is_feature_enabled('TEA_FEATURE_PDF_OCR'):
    @app.post("/pdf/ocr", response_model=List[TextExtract], tags=['pdf'])
    async def extract_text_with_ocr_from_pdf(
            file: UploadFile,
    ) -> Any:
        logger.debug(f"extract text with ocr from pdf file='{file.filename}'")
        pdf = PdfDataExtractor()
        return pdf.extract_text_with_ocr(data=await file.read(), filename=file.filename)

if is_feature_enabled('TEA_FEATURE_PDF_TABLE'):
    @app.post("/pdf/table", response_model=List[TableExtract], tags=['pdf'])
    async def extract_table_from_pdf(
            file: UploadFile,
    ) -> Any:
        logger.debug(f"extract table from pdf file='{file.filename}'")
        pdf = PdfDataExtractor()
        return pdf.extract_table(data=await file.read(), filename=file.filename)

if is_feature_enabled('TEA_FEATURE_CONVERT_PDFA_CONVERT'):
    @app.post("/pdfa/convert", response_class=FileResponse, tags=['pdfa'])
    async def convert_pdf_to_pdfa_with_ocr(
            file: UploadFile,
    ) -> Any:
        logger.debug(f"extract table from pdf file='{file.filename}'")
        pdf = PdfAConverter()
        return pdf.convert_pdfa(data=await file.read(), filename=file.filename)

if is_feature_enabled('TEA_FEATURE_CONVERT_PDFA_VALIDATE'):
    @app.post("/pdfa/validate", response_class=JSONResponse, tags=['pdfa'])
    async def convert_pdf_to_pdfa_with_ocr(
            file: UploadFile,
    ) -> Any:
        logger.debug(f"extract table from pdf file='{file.filename}'")
        pdf = PdfAValidator()
        return pdf.validate_pdf(data=await file.read(), filename=file.filename)

if is_feature_enabled('TEA_FEATURE_CONVERT_LIBREOFFICE'):
    @app.post("/libreoffice/convert", response_class=FileResponse, tags=['libreoffice'])
    async def convert_libreoffice_docs_to_pdf(
            file: UploadFile,
    ) -> Any:
        logger.debug(f"libreoffice convert file='{file.filename}' to pdf")
        libreoffice = LibreOfficeAdapter()
        return libreoffice.convert_to_pdf(data=await file.read(), filename=file.filename)


@app.post("/libreoffice/convert/remote", response_class=FileResponse, tags=['libreoffice'])
async def convert_libreoffice_docs_to_pdf(
        repo: HttpRemoteRepository,
) -> Any:
    file = None
    libreoffice = LibreOfficeAdapter()
    return libreoffice.convert_to_pdf(data=await file.read(), filename=file.filename)


def custom_openapi():
    tags_metadata = [
        {
            "name": "pdf",
            "description": "Extract text, OCR or tables from PDFs",
        },
        {
            "name": "pdfa",
            "description": "Convert PDFs to PDF/A.",
        },
        {
            "name": "libreoffice",
            "description": "Convert documents to PDF.",
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
