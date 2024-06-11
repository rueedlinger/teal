import logging
from typing import List, Any

from fastapi import APIRouter, UploadFile, Query

from teal import CheckUnknownQueryParamsRouter
from teal.core import is_feature_enabled
from teal.core.extract import PdfDataExtractor, PdfMetaDataExtractor
from teal.model.extract import TextExtract, ExtractMode, TableExtract, PdfMetaDataReport

_logger = logging.getLogger("teal.routers.extract")
router = APIRouter(prefix="/extract", tags=["extract"])

router.route_class = CheckUnknownQueryParamsRouter

if is_feature_enabled("TEAL_FEATURE_EXTRACT_TEXT"):
    _logger.info("feature PDF text is enabled")

    @router.post(
        "/text",
        summary="Extract text from a PDF",
        response_model=List[TextExtract],
    )
    async def extract_text_from_pdf(
        file: UploadFile,
        pages: str = Query(default=None),
        mode: ExtractMode = Query(default=None),
        languages: List[str] = Query([]),
    ) -> Any:
        _logger.debug(
            f"extract text from pdf file='{file.filename}', mode='{mode}',languages='{languages}',  pages='{pages}'"
        )
        pdf = PdfDataExtractor()
        if mode == ExtractMode.OCR:
            return pdf.extract_text_with_ocr(
                data=await file.read(),
                filename=file.filename,
                langs=languages,
                page_ranges=pages,
            )
        else:
            return pdf.extract_text(
                data=await file.read(), filename=file.filename, page_ranges=pages
            )


if is_feature_enabled("TEAL_FEATURE_EXTRACT_TABLE"):
    _logger.info("feature PDF table is enabled")

    @router.post(
        "/table",
        summary="Extract tables from a PDF",
        response_model=List[TableExtract],
    )
    async def extract_table_from_pdf(
        file: UploadFile,
        pages: str = Query(default=None),
    ) -> Any:
        _logger.debug(f"extract table from pdf file='{file.filename}', pages='{pages}'")
        pdf = PdfDataExtractor()
        return pdf.extract_table(
            data=await file.read(), filename=file.filename, page_ranges=pages
        )


if is_feature_enabled("TEAL_FEATURE_EXTRACT_META"):
    _logger.info("feature PDF meta data is enabled")

    @router.post(
        "/meta",
        summary="Extract metadata from a PDF",
        response_model=PdfMetaDataReport,
    )
    async def extract_text_from_pdf(
        file: UploadFile,
    ) -> Any:
        _logger.debug(f"extract meta data from pdf file='{file.filename}'")
        pdf = PdfMetaDataExtractor()
        return pdf.extract_meta_data(data=await file.read(), filename=file.filename)
