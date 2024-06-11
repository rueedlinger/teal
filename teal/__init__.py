import logging
import logging.config
import os

import yaml
from fastapi import FastAPI, Request

from teal.core import default_logging_conf
from teal.core.http import (
    create_json_err_response_from_exception,
    CheckUnknownQueryParamsRouter,
)
from teal.core.internal import AppPrometheusAdapter, OpenApiAdapter

logger = logging.getLogger("teal.api")


def init_logging():

    if "TEAL_LOG_CONF" in os.environ:
        log_conf_file = os.environ["TEAL_LOG_CONF"]
        with open(log_conf_file, "rt") as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
            logger.info(f"logging config loaded from {log_conf_file}")
    else:
        logging.config.dictConfig(default_logging_conf())
        logger.info(f"logging config file not set using default")


def create_app() -> FastAPI:

    init_logging()

    app = FastAPI()

    @app.exception_handler(Exception)
    async def unicorn_exception_handler(request: Request, ex: Exception):
        return create_json_err_response_from_exception(ex)

    @app.on_event("startup")
    async def startup_event():
        logger.info("startup")

    from teal.routers import extract, create, ocr, validate, internal

    app.include_router(extract.router)
    app.include_router(create.router)
    app.include_router(ocr.router)
    app.include_router(validate.router)
    app.include_router(internal.router)

    openapi_adapter = OpenApiAdapter(app)
    openapi_adapter.enable_openapi()

    prometheus_adapter = AppPrometheusAdapter(app)
    prometheus_adapter.enable_prometheus()

    return app
