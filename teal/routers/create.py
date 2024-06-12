import logging
from typing import Any

from fastapi import APIRouter, UploadFile, Query
from starlette.responses import FileResponse

from teal import CheckUnknownQueryParamsRouter
from teal.core import is_feature_enabled
from teal.core.create import LibreOfficeAdapter
from teal.model.create import OutputType

router = APIRouter(prefix="/create", tags=["create"])
_logger = logging.getLogger("teal.routers.create")

router.route_class = CheckUnknownQueryParamsRouter

if is_feature_enabled("TEAL_FEATURE_CREATE_PDF"):
    _logger.info("feature libreoffice convert is enabled")

    @router.post(
        "/pdf",
        summary="Create PDF or PDF/A documents",
        response_class=FileResponse,
    )
    async def create_pdf(
        file: UploadFile,
        output: OutputType = Query(default=None),
        pages: str = Query(default=None),
    ) -> Any:
        _logger.debug(
            f"create pdf file='{file.filename}', output={output}, pages='{pages}'"
        )

        libreoffice = LibreOfficeAdapter()
        return await libreoffice.create_pdf(
            data=await file.read(),
            filename=file.filename,
            output_type=output,
            page_ranges=pages,
        )
