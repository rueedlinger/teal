import logging.config
import os
from typing import Any, List

import yaml
from fastapi import FastAPI, UploadFile, Request, Query
from fastapi.openapi.utils import get_openapi
from starlette.responses import FileResponse

from teal.core import (
    create_json_err_response_from_exception,
    is_feature_enabled,
    get_version,
    get_tesseract_languages,
)
from teal.libreoffice import LibreOfficeAdapter
from teal.model import TextExtract, TableExtract, PdfAReport, PdfAProfile
from teal.pdf import PdfDataExtractor
from teal.pdfa import PdfAValidator, PdfAConverter

app = FastAPI()
logger = logging.getLogger("teal.api")
if "TEAL_LOG_CONF" in os.environ:
    log_conf_file = os.environ["TEAL_LOG_CONF"]
    with open(log_conf_file, "rt") as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
        logger.info(f"logging config loaded from {log_conf_file}")
else:
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "simple": {
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "simple",
                    "stream": "ext://sys.stdout",
                },
            },
            "loggers": {
                "teal": {"level": "INFO", "handlers": ["console"], "propagate": False},
                "uvicorn": {
                    "level": "INFO",
                    "handlers": ["console"],
                    "propagate": False,
                },
            },
            "root": {"handlers": ["console"], "level": "WARN"},
        }
    )
    logger.info(f"logging config file not set using default")


# get root logger
logger.info(f"installed tesseract languages: {get_tesseract_languages()}")


@app.exception_handler(Exception)
async def unicorn_exception_handler(request: Request, ex: Exception):
    return create_json_err_response_from_exception(ex)


if is_feature_enabled("TEA_FEATURE_PDF_TEXT"):
    logger.info("feature PDF text is enabled")

    @app.post("/pdf/text", response_model=List[TextExtract], tags=["pdf"])
    async def extract_text_from_pdf(
        file: UploadFile,
    ) -> Any:
        logger.debug(f"extract text from pdf file='{file.filename}'")
        pdf = PdfDataExtractor()
        return pdf.extract_text(data=await file.read(), filename=file.filename)


if is_feature_enabled("TEA_FEATURE_PDF_OCR"):
    logger.info("feature PDF ocr is enabled")

    @app.post("/pdf/ocr", response_model=List[TextExtract], tags=["pdf"])
    async def extract_text_with_ocr_from_pdf(
        file: UploadFile, languages: List[str] = Query([])
    ) -> Any:
        logger.debug(f"extract text with ocr from pdf file='{file.filename}'")
        pdf = PdfDataExtractor()
        return pdf.extract_text_with_ocr(
            data=await file.read(), filename=file.filename, langs=languages
        )


if is_feature_enabled("TEA_FEATURE_PDF_TABLE"):
    logger.info("feature PDF table is enabled")

    @app.post("/pdf/table", response_model=List[TableExtract], tags=["pdf"])
    async def extract_table_from_pdf(file: UploadFile) -> Any:
        logger.debug(f"extract table from pdf file='{file.filename}'")
        pdf = PdfDataExtractor()
        return pdf.extract_table(data=await file.read(), filename=file.filename)


if is_feature_enabled("TEA_FEATURE_CONVERT_PDFA_CONVERT"):
    logger.info("feature PDF/A convert is enabled")

    @app.post("/pdfa/convert", response_class=FileResponse, tags=["pdfa"])
    async def convert_pdf_to_pdfa_with_ocr(
        file: UploadFile,
        languages: List[str] = Query([]),
        pdfa: PdfAProfile = Query(PdfAProfile.PDFA1),
    ) -> Any:
        logger.debug(
            f"extract table from pdf file='{file.filename}', languages='{languages}, pdfa='{pdfa}'"
        )
        logger.info(languages)
        pdf = PdfAConverter()
        return pdf.convert_pdfa(
            data=await file.read(), filename=file.filename, langs=languages, pdfa=pdfa
        )


if is_feature_enabled("TEA_FEATURE_CONVERT_PDFA_VALIDATE"):
    logger.info("feature PDF/A validate is enabled")

    @app.post("/pdfa/validate", response_model=PdfAReport, tags=["pdfa"])
    async def validate_pdfa(
        file: UploadFile,
    ) -> Any:
        logger.debug(f"extract table from pdf file='{file.filename}'")
        pdf = PdfAValidator()
        return pdf.validate_pdf(data=await file.read(), filename=file.filename)


if is_feature_enabled("TEA_FEATURE_LIBREOFFICE_CONVERT"):
    logger.info("feature libreoffice convert is enabled")

    @app.post("/libreoffice/convert", response_class=FileResponse, tags=["libreoffice"])
    async def convert_libreoffice_docs_to_pdf(
        file: UploadFile,
    ) -> Any:
        logger.debug(f"libreoffice convert file='{file.filename}' to pdf")
        libreoffice = LibreOfficeAdapter()
        return libreoffice.convert_to_pdf(
            data=await file.read(), filename=file.filename
        )


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
        version=get_version(),
        summary="A convenient REST API for working with PDF's",
        description="**teal** aims to provide a user-friendly API for working with PDFs which can be easily integrated in an existing workflow. ",
        routes=app.routes,
        tags=tags_metadata,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
