import logging
from typing import Any

from fastapi import APIRouter, UploadFile, Query

from teal import CheckUnknownQueryParamsRouter
from teal.core import is_feature_enabled
from teal.core.pdfa import PdfAValidator
from teal.model.validate import PdfAReport, ValidatePdfProfile

router = APIRouter(prefix="/validate", tags=["validate"])
logger = logging.getLogger("teal.routers.validate")

router.route_class = CheckUnknownQueryParamsRouter

if is_feature_enabled("TEAL_FEATURE_VALIDATE_PDFA"):
    logger.info("feature PDF/A validate is enabled")

    @router.post(
        "/pdfa",
        summary="Validate PDF documents for PDF/A compliance",
        response_model=PdfAReport,
    )
    async def validate_pdfa(
        file: UploadFile,
        profile: ValidatePdfProfile = Query(default=None),
    ) -> Any:
        logger.debug(
            f"extract table from pdf file='{file.filename}', profile='{profile}'"
        )
        pdf = PdfAValidator()
        return await pdf.validate_pdf(
            data=await file.read(), filename=file.filename, profile=profile
        )
