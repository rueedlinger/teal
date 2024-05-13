import json
import logging
import os
import shutil
import subprocess
import tempfile

import camelot.io as camelot
import pypdfium2 as pdfium
import pytesseract
from pdf2image import convert_from_bytes
from starlette.background import BackgroundTask
from starlette.responses import FileResponse

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


class PdfAConverter:
    def __init__(self, ocrmypdf_cmd='ocrmypdf'):
        self.ocrmypdf_cmd = ocrmypdf_cmd
        self.supported_file_extensions = ['.pdf']

    def convert_pdf(self, data, filename):
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in self.supported_file_extensions:
            return create_json_err_response(400, f"file extension '{file_ext}' is not supported ({filename}).")

        # create tmp dir for all files
        tmp_dir = tempfile.mktemp(prefix='teal-')
        _logger.debug(f"creating tmp dir: {tmp_dir}")
        os.mkdir(tmp_dir)

        tmp_file_in_path = os.path.join(tmp_dir, "in-tmp.pdf")
        tmp_file_out_path = os.path.join(tmp_dir, "out-tmp.pdf")

        with open(tmp_file_in_path, 'wb') as tmp_file_in:
            _logger.debug(f"writing file {filename} to {tmp_file_in_path}")
            tmp_file_in.write(data)

        # see https://ocrmypdf.readthedocs.io/en/latest/advanced.html
        # -l eng+fra
        # --output-type {pdfa,pdf,pdfa-1,pdfa-2,pdfa-3,non
        # --skip-text then no image processing or OCR will be performed on pages that already
        # have text. The page will be copied to the output. This may be useful for documents that contain
        # both “born digital” and scanned content, or to use OCRmyPDF to normalize and convert to PDF/A
        # regardless of their contents.

        cmd_convert_pdf = f'{self.ocrmypdf_cmd} --skip-text --output-type pdfa "{tmp_file_in_path}" "{tmp_file_out_path}"'

        _logger.debug(f"running cmd: {cmd_convert_pdf}")
        result = subprocess.run(cmd_convert_pdf, shell=True, capture_output=True, env={'HOME': '/tmp'})

        if os.path.exists(tmp_file_out_path):
            _logger.debug(f"out was written {tmp_file_out_path}")
            return FileResponse(tmp_file_out_path, media_type='application/pdf',
                                filename=f"{os.path.splitext(filename)[0]}.pdf",
                                background=BackgroundTask(_cleanup_tmp_dir, tmp_dir))

        else:
            _logger.debug(f"file was not written {result}")
            return create_json_err_response(500, f"could not convert file '{filename}' ({result}).")


def _cleanup_tmp_dir(tmp_dir: str):
    teal_tmp_dir_prefix = '/tmp/teal-'
    if tmp_dir.startswith(teal_tmp_dir_prefix):
        _logger.debug(f"cleanup tmp dir {tmp_dir}")
        shutil.rmtree(tmp_dir)
    else:
        _logger.warning(f"will not delete '{tmp_dir}', tmp dir mus start with '{teal_tmp_dir_prefix}'")
