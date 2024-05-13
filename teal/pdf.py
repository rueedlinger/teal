import json
import logging
import os
import tempfile

import camelot.io as camelot
import pypdfium2 as pdfium
import pytesseract
from pdf2image import convert_from_bytes

from teal.core import create_json_err_response
from teal.model import TextExtract, TableExtract

_logger = logging.getLogger("teal.pdf")


class PdfDataExtractor:
    def __init__(self):
        self.supported_file_extensions = ['.pdf']

    def extract_text(self, data, filename):
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in self.supported_file_extensions:
            return create_json_err_response(400, f"file extension '{file_ext}' is not supported ({filename}).")

        extracts = []
        pdf = pdfium.PdfDocument(data)
        _logger.debug(f"found {len(pdf)} pages with pdf")
        for p in range(len(pdf)):
            textpage = pdf[p].get_textpage()
            text_all = textpage.get_text_bounded()
            extracts.append(TextExtract.parse_obj({"text": text_all, "page": p + 1}))

        return extracts

    def extract_text_with_ocr(self, data, filename, lang=None, first_page=None, last_page=None):
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in self.supported_file_extensions:
            return create_json_err_response(400, f"file extension '{file_ext}' is not supported ({filename}).")

        extracts = []
        images = convert_from_bytes(data)
        _logger.debug(f"made {len(images)} images with pdf2images")

        for i, page in enumerate(images):
            # multi lang eg. eng+chi_tra
            text = pytesseract.image_to_string(page, lang=lang)
            extracts.append(TextExtract.parse_obj({"text": text, "page": i + 1}))
        return extracts

    def extract_table(self, data, filename):
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in self.supported_file_extensions:
            return create_json_err_response(400, f"file extension '{file_ext}' is not supported ({filename}).")

        with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp_pdf_file:
            tmp_pdf_file.write(data)
            tables = camelot.read_pdf(tmp_pdf_file.name, pages="all")
            _logger.debug(f"found {len(tables)} tables with camelot")
            extracts = []

            for p in range(len(tables)):
                with tempfile.NamedTemporaryFile(suffix=".json") as tmp_json_file:
                    tables[p].to_json(tmp_json_file.name)
                    report = tables[p].parsing_report
                    _logger.debug(f"parsing tables report {report}")
                    f = open(tmp_json_file.name)
                    table_json = json.load(f)
                    extracts.append(
                        TableExtract.parse_obj(
                            {
                                "page": report["page"],
                                "index": report["order"] - 1,
                                "table": table_json,
                            }
                        )
                    )
                    f.close()

        return extracts
