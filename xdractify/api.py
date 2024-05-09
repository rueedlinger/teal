import base64
import binascii
import logging
from typing import Any, List

from fastapi import FastAPI, UploadFile, Request
from starlette.responses import JSONResponse

from xdractify.model import (
    Document,
    DataEncoding,
    Data,
    TextExtract,
    TableExtract,
)
from xdractify.pdf import PdfModule

# get root logger
logger = logging.getLogger("xdractify.api")

app = FastAPI()


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


@app.get("/modules")
async def get_modules() -> dict[str, List[tuple[str, str]]]:
    return {"pdf": PdfModule().get_modules()}


@app.post("/pdf/{module}/text", response_model=List[TextExtract])
async def extract_text_from_pdf(
    request: Request,
    file: UploadFile,
    module: str,
) -> Any:

    logger.debug(f"processing pdf, module='{module}'")
    pdf = PdfModule()

    return pdf.run(
        module=module,
        action="text",
        data=await file.read(),
        params=request.query_params,
    )


@app.post("/pdf/{module}/table", response_model=List[TableExtract])
async def extract_table_from_pdf(
    request: Request,
    file: UploadFile,
    module: str,
) -> Any:

    logger.debug(f"processing pdf, module='{module}'")
    pdf = PdfModule()

    return pdf.run(
        module=module,
        action="table",
        data=await file.read(),
        params=request.query_params,
    )


@app.post("/base64/encode", response_model=Document)
async def encode_file_to_base64(file: UploadFile) -> Any:
    logger.debug(
        f"base64 encode: filename='{file.filename}', size='{file.size}', content_type='{file.content_type}'"
    )
    contents = await file.read()
    encoded = base64.b64encode(contents)
    return Document.parse_obj(
        {
            "name": file.filename,
            "data": Data.parse_obj(
                {"encoding": DataEncoding.base64, "content": encoded}
            ),
        }
    )


"""
@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}
"""
