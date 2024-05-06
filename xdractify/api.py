import binascii
from typing import Union, Annotated

from fastapi import FastAPI, UploadFile, File, Request
from pydantic import BaseModel
from starlette.responses import JSONResponse

from xdractify.model import Document, PdfDocument, DataEncoding
import logging
import base64

# get root logger
logger = logging.getLogger('xdractify.api')

app = FastAPI()


@app.exception_handler(binascii.Error)
async def unicorn_exception_handler(request: Request, ex: binascii.Error):
    return JSONResponse(
        status_code=400,
        content={"message": f"bas46 error, {ex}"},
    )


@app.post("/pdf")
async def read_item(doc: PdfDocument):
    logger.debug(f"processing pdf: {doc}")
    if doc.encoding == DataEncoding.base64:
        raw = base64.b64decode(doc.data)
        logger.debug(raw)
    return {}


@app.post("/base64/encode")
async def input_request(file: UploadFile) -> Document:
    contents = await file.read()
    encoded = base64.b64encode(contents)
    return Document.parse_obj({'name': file.filename, 'data': encoded, 'encoding': DataEncoding.base64})


"""
@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}
"""
