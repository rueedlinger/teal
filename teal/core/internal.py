import logging
import os
from typing import Callable

import PyPDF2
import camelot
import cv2
import fastapi
import pikepdf
import pypdfium2
import pytesseract
from fastapi.openapi.utils import get_openapi
from prometheus_fastapi_instrumentator import Instrumentator, metrics
from starlette.applications import Starlette

from teal.core import get_tesseract_languages, get_version, is_feature_enabled
from teal.model.internal import AppInfo, HealthCheck

_logger = logging.getLogger("teal.internal")


class AppAdapter:

    def get_app_info(self) -> AppInfo:

        details = {}
        for k in os.environ.keys():
            if k.startswith("TEAL_"):
                details[k.lower().replace("teal_", "")] = os.environ[k]

        details["tesseract_languages"] = get_tesseract_languages()

        self.add_app_detail(details, "pikepdf_version", lambda: pikepdf.__version__)
        self.add_app_detail(
            details, "pytesseract_version", lambda: pytesseract.__version__
        )
        self.add_app_detail(details, "pypdf2_version", lambda: PyPDF2.__version__)
        self.add_app_detail(details, "pypdfium2_version", lambda: pypdfium2.V_PYPDFIUM2)
        self.add_app_detail(details, "camelot_version", lambda: camelot.__version__)
        self.add_app_detail(details, "fastapi_version", lambda: fastapi.__version__)
        self.add_app_detail(details, "opencv_version", lambda: cv2.__version__)

        return AppInfo.model_validate({"version": get_version(), "details": details})

    @staticmethod
    def add_app_detail(details: dict, key: str, func: Callable[[], str]):
        try:
            details[key] = func()
        except Exception as e:
            details[key] = str(e)

    def get_health_check(self) -> HealthCheck:
        return HealthCheck(status="OK")


class AppPrometheusAdapter:

    def __init__(self, app: Starlette):
        self.app = app

    def enable_prometheus(self):
        if is_feature_enabled("TEAL_FEATURE_APP_METRICS"):
            _logger.info("enabling prometheus metrics")
            instrumentator = Instrumentator(
                excluded_handlers=["/app/*", "/docs/*", "/openapi.json"]
            )
            instrumentator.instrument(self.app).expose(
                self.app,
                endpoint="/app/metrics",
                tags=["app"],
                include_in_schema=True,
            )
            instrumentator.add(metrics.requests())


class OpenApiAdapter:

    def __init__(self, app):
        self.app = app

    def custom_openapi(self):
        tags_metadata = [
            {
                "name": "extract",
                "description": "Endpoints for extracting text, tables, and metadata from PDFs.",
            },
            {
                "name": "create",
                "description": "Endpoint for creating PDF or PDF/A documents.",
            },
            {
                "name": "ocr",
                "description": "Endpoint for converting PDFs to searchable PDF or PDF/A using OCR.",
            },
            {
                "name": "validate",
                "description": "Endpoint for validating PDF/A compliance.",
            },
            {
                "name": "app",
                "description": "Endpoints for application health, information, and metrics.",
            },
        ]

        if self.app.openapi_schema:
            return self.app.openapi_schema
        openapi_schema = get_openapi(
            title="teal",
            version=get_version(),
            summary="A convenient REST API for working with PDF's",
            description="**teal** aims to provide a user-friendly API for working with PDFs which can be easily integrated in an existing workflow. ",
            routes=self.app.routes,
            tags=tags_metadata,
        )
        openapi_schema["info"]["x-logo"] = {
            "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
        }
        self.app.openapi_schema = openapi_schema
        return self.app.openapi_schema

    def enable_openapi(self):
        self.app.openapi = self.custom_openapi
