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
from teal.pdf import PdfDataExtractor

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


"""
@app.get("/")
async def redirect_typer():
    return RedirectResponse("/docs")
"""


@app.post("/pdf/text", response_model=List[TextExtract])
async def extract_text_from_pdf(
        file: UploadFile,
) -> Any:
    logger.debug(f"extract text from pdf file='{file.filename}'")
    pdf = PdfDataExtractor()
    return pdf.extract_text(data=await file.read(), filename=file.filename)


@app.post("/pdf/ocr", response_model=List[TextExtract])
async def extract_text_with_ocr_from_pdf(
        file: UploadFile,
) -> Any:
    logger.debug(f"extract text with ocr from pdf file='{file.filename}'")
    pdf = PdfDataExtractor()
    return pdf.extract_text_with_ocr(data=await file.read(), filename=file.filename)


@app.post("/pdf/table", response_model=List[TableExtract])
async def extract_table_from_pdf(
        file: UploadFile,
) -> Any:
    logger.debug(f"extract table from pdf file='{file.filename}'")
    pdf = PdfDataExtractor()
    return pdf.extract_table(data=await file.read(), filename=file.filename)


@app.post("/pdf/convert", response_model=List[str])
async def convert_pdf(
        file: UploadFile,
) -> Any:
    logger.debug(f"extract table from pdf file='{file.filename}'")

    return []


@app.post("/libreoffice/pdf", response_class=FileResponse)
async def convert_libreoffice_to_pdf(
        file: UploadFile,
) -> Any:
    logger.debug(f"libreoffice convert file='{file.filename}' to pdf")
    libreoffice = LibreOfficeAdapter()
    return libreoffice.convert_to_pdf(data=await file.read(), filename=file.filename)


"""
@app.post("/pdf/meta", response_model=List[dict])
async def extract_meta_data_from_pdf(
        file: UploadFile,
) -> Any:
    logger.debug(f"extract meta data from pdf file='{file.filename}'")
    pdf = PdfMetaDataExtractor()
    return pdf.extract_metadata(data=await file.read())

@app.post("/base64/encode", response_model=Document)
async def encode_file_to_base64(file: UploadFile) -> Any:
    logger.debug(
        f"base64 encode: filename='{file.filename}', size='{file.size}', content_type='{file.content_type}'"
    )
    b64 = Base64()
    return b64.encode(data=await file.read(), filename=file.filename)
"""


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="teal",
        version="0.1.0",
        summary="A convenient REST API for working with PDF's",
        description="**teal** aims to provide a user-friendly API for working with PDFs which can be easily integrated in an existing workflow. ",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
