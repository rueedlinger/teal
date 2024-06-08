import io
import json
import logging
import os
import tempfile

import camelot.io as camelot
import pikepdf
import pypdfium2 as pdfium
import pytesseract
from pdf2image import convert_from_bytes
from starlette.responses import JSONResponse

from teal.core import (
    make_tesseract_lang_param,
    parse_page_ranges,
)
from teal.http import create_json_err_response
from teal.model import TextExtract, TableExtract, PdfMetaDataReport

_logger = logging.getLogger("teal.pdf")


class PdfDataExtractor:
    def __init__(self):
        self.supported_file_extensions = [".pdf"]

    def extract_text(
        self,
        data: bytes,
        filename: str,
        page_ranges: str,
    ) -> list[TextExtract] | JSONResponse:
        file_ext = os.path.splitext(filename)[1]
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
                    TextExtract.model_validate({"text": text_all, "page": page_no})
                )

        return extracts

    def extract_text_with_ocr(
        self,
        data: bytes,
        filename: str,
        langs: list[str],
        page_ranges: str,
    ) -> list[TextExtract] | JSONResponse:
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in self.supported_file_extensions:
            return create_json_err_response(
                400, f"file extension '{file_ext}' is not supported ({filename})."
            )

        extracts = []
        images = convert_from_bytes(data)
        _logger.debug(f"made {len(images)} images with pdf2images")

        pages = parse_page_ranges(page_ranges)

        for i, page in enumerate(images):
            page_no = i + 1
            if pages is None or page_no in pages:
                languages = make_tesseract_lang_param(langs)
                if languages is None:
                    languages = "eng"
                text = pytesseract.image_to_string(page, lang=languages)
                extracts.append(
                    TextExtract.model_validate({"text": text, "page": page_no})
                )
        return extracts

    def extract_table(
        self,
        data: bytes,
        filename: str,
        page_ranges: str,
    ) -> list[TableExtract] | JSONResponse:
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in self.supported_file_extensions:
            return create_json_err_response(
                400, f"file extension '{file_ext}' is not supported ({filename})."
            )

        with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp_pdf_file:
            tmp_pdf_file.write(data)
            tables = camelot.read_pdf(tmp_pdf_file.name, pages="all")
            _logger.debug(f"found {len(tables)} tables with camelot")
            extracts = []

            pages = parse_page_ranges(page_ranges)

            for p in range(len(tables)):
                with tempfile.NamedTemporaryFile(suffix=".json") as tmp_json_file:
                    tables[p].to_json(tmp_json_file.name)
                    report = tables[p].parsing_report
                    page_no = report["page"]
                    if pages is None or page_no in pages:
                        _logger.debug(f"parsing tables report {report}")
                        f = open(tmp_json_file.name)
                        table_json = json.load(f)
                        extracts.append(
                            TableExtract.model_validate(
                                {
                                    "page": page_no,
                                    "index": report["order"] - 1,
                                    "table": table_json,
                                }
                            )
                        )
                        f.close()

        return extracts


class PdfMetaDataExtractor:
    def __init__(self):
        self.supported_file_extensions = [".pdf"]

    def extract_meta_data(
        self,
        data: bytes,
        filename: str,
    ) -> PdfMetaDataReport | JSONResponse:
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in self.supported_file_extensions:
            return create_json_err_response(
                400, f"file extension '{file_ext}' is not supported ({filename})."
            )
        meta_data = {}
        pdf = pikepdf.open(io.BytesIO(data))
        meta = pdf.open_metadata()
        for m in meta:
            meta_data[m] = meta.get(m)

        doc_info = {}
        for key, value in pdf.docinfo.items():
            doc_info[key] = str(value)
        pdf.close()
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
