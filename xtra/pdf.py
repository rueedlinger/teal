import json
import logging
import tempfile
from io import BytesIO

import camelot.io as camelot
import pikepdf
import pypdfium2 as pdfium
import pytesseract
from pdf2image import convert_from_bytes

from xtra.model import TextExtract, TableExtract

_logger = logging.getLogger("xtra.pdf")


def extract_table(data, params):
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
                            "index": report["order"],
                            "table": table_json,
                        }
                    )
                )
                f.close()

    return extracts


class PdfTextExtractor:
    def __init__(self):
        pass

    def extract_text_pypdfium(self, data):
        extracts = []
        pdf = pdfium.PdfDocument(data)
        _logger.debug(f"found {len(pdf)} pages with pdf")
        for p in range(len(pdf)):
            textpage = pdf[p].get_textpage()
            text_all = textpage.get_text_bounded()
            extracts.append(TextExtract.parse_obj({"text": text_all, "page": p + 1}))

        return extracts


class PdfOcrExtractor:
    def __init__(self):
        pass

    def extract_text(self, data, lang=None, first_page=None, last_page=None):
        extracts = []
        images = convert_from_bytes(data)
        _logger.debug(f"made {len(images)} images with pdf2images")

        for i, page in enumerate(images):
            text = pytesseract.image_to_string(page, lang=lang)
            extracts.append(TextExtract.parse_obj({"text": text, "page": i + 1}))
        return extracts


class PdfTableExtractor:
    def __init__(self):
        pass

    def extract_table(self, data):
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


class PdfMetaDataExtractor:
    def __init__(self):
        pass

    def extract_metadata(self, data):
        pdf = pikepdf.open(BytesIO(data))
        extarct = []

        doc_info = {}
        for k in pdf.docinfo.keys():
            doc_info[k] = str(pdf.docinfo.get(k))
        extarct.append({'document_info': doc_info})

        meta = pdf.open_metadata()
        extarct.append({'claimn_pdfa': meta.pdfa_status})
        extarct.append({'claimn_pdfx': meta.pdfx_status})

        return extarct
