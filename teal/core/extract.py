import io
import json
import logging
import os

import aiofiles
import aiopytesseract
import camelot.io as camelot
import pikepdf
import pypdfium2 as pdfium
from pdf2image import convert_from_path
from starlette.responses import JSONResponse

from teal.core import (
    make_tesseract_lang_param,
    parse_page_ranges,
    get_tesseract_languages,
    get_file_ext,
)
from teal.core.http import create_json_err_response
from teal.model.extract import TextExtract, TableExtract, PdfMetaDataReport, ExtractMode

_logger = logging.getLogger("teal.pdf")


class PdfDataExtractor:
    def __init__(self):
        self.supported_file_extensions = [".pdf"]
        self.supported_languages = get_tesseract_languages()

    async def extract_text(
        self,
        data: bytes,
        filename: str,
        page_ranges: str,
    ) -> list[TextExtract] | JSONResponse:
        file_ext = get_file_ext(filename)
        if file_ext not in self.supported_file_extensions:
            return create_json_err_response(
                400, f"file extension '{file_ext}' is not supported ({filename})."
            )

        extracts = []
        pdf = pdfium.PdfDocument(data)
        _logger.debug(f"found {len(pdf)} pages with pdf")

        pages = parse_page_ranges(page_ranges)

        for p in range(len(pdf)):
            page_no = p + 1
            if pages is None or page_no in pages:
                textpage = pdf[p].get_textpage()
                text_all = textpage.get_text_bounded()
                extracts.append(
                    TextExtract.model_validate(
                        {"text": text_all, "page": page_no, "mode": ExtractMode.RAW}
                    )
                )

        return extracts

    async def extract_text_with_ocr(
        self,
        data: bytes,
        filename: str,
        langs: list[str],
        page_ranges: str,
    ) -> list[TextExtract] | JSONResponse:
        file_ext = get_file_ext(filename)
        if file_ext not in self.supported_file_extensions:
            return create_json_err_response(
                400, f"file extension '{file_ext}' is not supported ({filename})."
            )

        extracts = []
        async with aiofiles.tempfile.TemporaryDirectory() as tmp_dir:
            async with aiofiles.open(
                os.path.join(tmp_dir, "in.pdf"), mode="wb"
            ) as tmp_file:
                await tmp_file.write(data)
                await tmp_file.flush()

                _logger.debug(f"in file: {tmp_file.name}, tmp_dir: {tmp_dir}")
                images = convert_from_path(
                    tmp_file.name, output_folder=tmp_dir, paths_only=True
                )

                _logger.debug(f"made {len(images)} images with pdf2images")
                pages = parse_page_ranges(page_ranges)

                for i, page in enumerate(images):
                    page_no = i + 1
                    if pages is None or page_no in pages:
                        languages = make_tesseract_lang_param(langs)
                        if languages is None:
                            languages = "eng"
                        text = await aiopytesseract.image_to_string(
                            page, lang=languages
                        )
                        extracts.append(
                            TextExtract.model_validate(
                                {"text": text, "page": page_no, "mode": ExtractMode.OCR}
                            )
                        )
        return extracts

    async def extract_table(
        self,
        data: bytes,
        filename: str,
        page_ranges: str,
    ) -> list[TableExtract] | JSONResponse:
        file_ext = get_file_ext(filename)
        if file_ext not in self.supported_file_extensions:
            return create_json_err_response(
                400, f"file extension '{file_ext}' is not supported ({filename})."
            )

        async with aiofiles.tempfile.NamedTemporaryFile(suffix=".pdf") as tmp_pdf_file:
            await tmp_pdf_file.write(data)
            tables = camelot.read_pdf(tmp_pdf_file.name, pages="all")
            _logger.debug(f"found {len(tables)} tables with camelot")
            extracts = []

            pages = parse_page_ranges(page_ranges)

            for p in range(len(tables)):
                async with aiofiles.tempfile.NamedTemporaryFile(
                    suffix=".json"
                ) as tmp_json_file:
                    tables[p].to_json(tmp_json_file.name)
                    report = tables[p].parsing_report
                    page_no = report["page"]
                    if pages is None or page_no in pages:
                        _logger.debug(f"parsing tables report {report}")
                        async with aiofiles.open(tmp_json_file.name) as f:
                            content = await f.read()
                            table_json = json.loads(content)
                            extracts.append(
                                TableExtract.model_validate(
                                    {
                                        "page": page_no,
                                        "index": report["order"] - 1,
                                        "table": table_json,
                                    }
                                )
                            )

        return extracts


class PdfMetaDataExtractor:
    def __init__(self):
        self.supported_file_extensions = [".pdf"]

    async def extract_meta_data(
        self,
        data: bytes,
        filename: str,
    ) -> PdfMetaDataReport | JSONResponse:
        file_ext = get_file_ext(filename)
        if file_ext not in self.supported_file_extensions:
            return create_json_err_response(
                400, f"file extension '{file_ext}' is not supported ({filename})."
            )
        meta_data = {}
        doc_info = {}
        with pikepdf.open(io.BytesIO(data)) as pdf:
            with pdf.open_metadata() as meta:
                for m in meta:
                    meta_data[m] = meta.get(m)

                for key, value in pdf.docinfo.items():
                    doc_info[key] = str(value)
        return PdfMetaDataReport.model_validate(
            {
                "fileName": filename,
                "fileSize": len(data),
                "pdfVersion": pdf.pdf_version,
                "pdfaClaim": (
                    None if meta.pdfa_status == "" else str(meta.pdfa_status)
                ),
                "pages": len(pdf.pages),
                "docInfo": doc_info,
                "xmp": meta_data,
            }
        )
