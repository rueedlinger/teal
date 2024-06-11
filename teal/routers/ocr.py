import logging
from typing import List, Any

from fastapi import APIRouter, UploadFile, Query
from starlette.responses import FileResponse

from teal import CheckUnknownQueryParamsRouter
from teal.core import is_feature_enabled
from teal.core.ocr import PdfOcrAdapter
from teal.model.ocr import OutputType, OcrMode

router = APIRouter(prefix="/ocr", tags=["ocr"])
_logger = logging.getLogger("teal.routers.ocr")

router.route_class = CheckUnknownQueryParamsRouter

if is_feature_enabled("TEAL_FEATURE_CREATE_PDFA"):
    _logger.info("feature PDF/A convert is enabled")

    @router.post(
        "/pdf",
        summary="Convert PDF documents to PDF/A",
        response_class=FileResponse,
    )
    async def create_pdf(
        file: UploadFile,
        languages: List[str] = Query(default=None),
        output: OutputType = Query(default=None),
        ocr: OcrMode = Query(default=None),
        pages: str = Query(default=None),
    ) -> Any:
        _logger.debug(
            f"extract table from pdf file='{file.filename}', languages='{languages}, output='{output}', ocr={ocr}, pages='{pages}'"
        )
        pdf = PdfOcrAdapter()
        return pdf.create_pdf(
            data=await file.read(),
            filename=file.filename,
            langs=languages,
            output_type=output,
            ocr_mode=ocr,
            page_ranges=pages,
        )
