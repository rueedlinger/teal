import logging.config
import os
from typing import Any, List

import yaml
from fastapi import FastAPI, UploadFile, Request, Query
from fastapi.openapi.utils import get_openapi
from prometheus_fastapi_instrumentator import Instrumentator, metrics
from starlette.responses import FileResponse

from teal.core import (
    is_feature_enabled,
    get_version,
    get_tesseract_languages,
    get_app_info,
)
from teal.http import (
    create_json_err_response_from_exception,
    CheckUnknownQueryParamsRouter,
)
from teal.libreoffice import LibreOfficeAdapter
from teal.model import (
    TextExtract,
    TableExtract,
    PdfAReport,
    OcrPdfAProfile,
    LibreOfficePdfProfile,
    HealthCheck,
    ValidatePdfProfile,
    PdfMetaDataReport,
    OcrMode,
    AppInfo,
)
from teal.pdf import PdfDataExtractor, PdfMetaDataExtractor
from teal.pdfa import PdfAValidator, PdfAConverter

app = FastAPI()
app.router.route_class = CheckUnknownQueryParamsRouter

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


if is_feature_enabled("TEAL_FEATURE_PDF_TEXT"):
    logger.info("feature PDF text is enabled")

    @app.post(
        "/pdf/text",
        summary="Extract text from a PDF",
        response_model=List[TextExtract],
        tags=["pdf"],
    )
    async def extract_text_from_pdf(
        file: UploadFile,
        pages: str = Query(default=None),
    ) -> Any:
        logger.debug(f"extract text from pdf file='{file.filename}', pages='{pages}'")
        pdf = PdfDataExtractor()
        return pdf.extract_text(
            data=await file.read(), filename=file.filename, page_ranges=pages
        )


if is_feature_enabled("TEAL_FEATURE_PDF_OCR"):
    logger.info("feature PDF ocr is enabled")

    @app.post(
        "/pdf/ocr",
        summary="Extract text with OCR from a PDF",
        response_model=List[TextExtract],
        tags=["pdf"],
    )
    async def extract_text_with_ocr_from_pdf(
        file: UploadFile,
        languages: List[str] = Query([]),
        pages: str = Query(default=None),
    ) -> Any:
        logger.debug(
            f"extract text with ocr from pdf file='{file.filename}', languages='{languages}', pages='{pages}'"
        )
        pdf = PdfDataExtractor()
        return pdf.extract_text_with_ocr(
            data=await file.read(),
            filename=file.filename,
            langs=languages,
            page_ranges=pages,
        )


if is_feature_enabled("TEAL_FEATURE_PDF_TABLE"):
    logger.info("feature PDF table is enabled")

    @app.post(
        "/pdf/table",
        summary="Extract tables from a PDF",
        response_model=List[TableExtract],
        tags=["pdf"],
    )
    async def extract_table_from_pdf(
        file: UploadFile,
        pages: str = Query(default=None),
    ) -> Any:
        logger.debug(f"extract table from pdf file='{file.filename}', pages='{pages}'")
        pdf = PdfDataExtractor()
        return pdf.extract_table(
            data=await file.read(), filename=file.filename, page_ranges=pages
        )


if is_feature_enabled("TEAL_FEATURE_PDF_META"):
    logger.info("feature PDF meta data is enabled")

    @app.post(
        "/pdf/meta",
        summary="Extract metadata from a PDF",
        response_model=PdfMetaDataReport,
        tags=["pdf"],
    )
    async def extract_text_from_pdf(
        file: UploadFile,
    ) -> Any:
        logger.debug(f"extract meta data from pdf file='{file.filename}'")
        pdf = PdfMetaDataExtractor()
        return pdf.extract_meta_data(data=await file.read(), filename=file.filename)


if is_feature_enabled("TEAL_FEATURE_PDFA_CONVERT"):
    logger.info("feature PDF/A convert is enabled")

    @app.post(
        "/pdfa/convert",
        summary="Convert PDF documents to PDF/A",
        response_class=FileResponse,
        tags=["pdfa"],
    )
    async def convert_pdf_to_pdfa_with_ocr(
        file: UploadFile,
        languages: List[str] = Query(default=None),
        profile: OcrPdfAProfile = Query(default=None),
        ocr: OcrMode = Query(default=None),
        pages: str = Query(default=None),
    ) -> Any:
        logger.debug(
            f"extract table from pdf file='{file.filename}', languages='{languages}, profile='{profile}', ocr={ocr}, pages='{pages}'"
        )
        pdf = PdfAConverter()
        return pdf.convert_pdfa(
            data=await file.read(),
            filename=file.filename,
            langs=languages,
            pdfa_profile=profile,
            ocr_mode=ocr,
            page_ranges=pages,
        )


if is_feature_enabled("TEAL_FEATURE_PDFA_VALIDATE"):
    logger.info("feature PDF/A validate is enabled")

    @app.post(
        "/pdfa/validate",
        summary="Validate PDF documents for PDF/A compliance",
        response_model=PdfAReport,
        tags=["pdfa"],
    )
    async def validate_pdfa(
        file: UploadFile,
        profile: ValidatePdfProfile = Query(default=None),
    ) -> Any:
        logger.debug(
            f"extract table from pdf file='{file.filename}', profile='{profile}'"
        )
        pdf = PdfAValidator()
        return pdf.validate_pdf(
            data=await file.read(), filename=file.filename, profile=profile
        )


if is_feature_enabled("TEAL_FEATURE_LIBREOFFICE_CONVERT"):
    logger.info("feature libreoffice convert is enabled")

    @app.post(
        "/libreoffice/convert",
        summary="Convert LibreOffice documents to PDF or PDF/A",
        response_class=FileResponse,
        tags=["libreoffice"],
    )
    async def convert_libreoffice_docs_to_pdf(
        file: UploadFile,
        profile: LibreOfficePdfProfile = Query(default=None),
        pages: str = Query(default=None),
    ) -> Any:
        logger.debug(
            f"libreoffice convert to pdf file='{file.filename}', profile={profile}, pages='{pages}'"
        )
        libreoffice = LibreOfficeAdapter()
        return libreoffice.convert_to_pdf(
            data=await file.read(),
            filename=file.filename,
            pdf_profile=profile,
            page_ranges=pages,
        )


if is_feature_enabled("TEAL_FEATURE_APP_HEALTH"):

    @app.get(
        "/app/health",
        tags=["app"],
        summary="Health Check",
        response_model=HealthCheck,
    )
    def get_health() -> HealthCheck:
        return HealthCheck(status="OK")


if is_feature_enabled("TEAL_FEATURE_APP_INFO"):

    @app.get(
        "/app/info",
        tags=["app"],
        summary="Application information's",
        response_model=AppInfo,
    )
    def get_health() -> AppInfo:
        return get_app_info()


def custom_openapi():
    tags_metadata = [
        {
            "name": "pdf",
            "description": "Extract text, perform OCR, or extract tables from PDFs.",
        },
        {
            "name": "pdfa",
            "description": "Convert PDF to PDF/A and validate PDF/A compliance.",
        },
        {
            "name": "libreoffice",
            "description": "Convert LibreOffice documents to PDF.",
        },
        {
            "name": "app",
            "description": "Application information.",
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

if is_feature_enabled("TEAL_FEATURE_APP_METRICS"):
    instrumentator = Instrumentator(
        excluded_handlers=["/app/*", "/docs/*", "/openapi.json"]
    )
    instrumentator.instrument(app).expose(
        app, endpoint="/app/metrics", include_in_schema=True, tags=["app"]
    )
    instrumentator.add(metrics.requests())
