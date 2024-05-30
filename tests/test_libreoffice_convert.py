import json
import os

from starlette.responses import FileResponse, JSONResponse

import teal.libreoffice as libreoffice
import teal.pdf as pdf
import teal.pdfa as pdfa
from teal.model import LibreOfficePdfProfile
from tests import load_file


def test_non_zero_return_code():
    converter = libreoffice.LibreOfficeAdapter()
    converter.libreoffice_cmd = "foo"
    resp = converter.convert_to_pdf(
        load_file("data/doc/normal_document.docx"), "test.docx"
    )
    assert type(resp) is JSONResponse
    assert resp.status_code == 500
    print(json.loads(resp.body))
    assert json.loads(resp.body) == {
        "message": "got return code 127 'test.docx' /bin/sh: 1: foo: not found\n"
    }


def test_not_supported_types():
    converter = libreoffice.LibreOfficeAdapter()
    resp = converter.convert_to_pdf("", "test.zip")
    assert type(resp) is JSONResponse
    assert resp.status_code == 400
    assert json.loads(resp.body) == {
        "message": "file extension '.zip' is not supported (test.zip)."
    }


def test_convert_to_pdf_15_with_version_from_docx():
    resp = _convert_to_pdf_version(LibreOfficePdfProfile.PDF15)

    assert type(resp) is JSONResponse
    assert resp.status_code == 200
    json_resp = json.loads(resp.body)

    assert json_resp["compliant"] is False
    assert json_resp["profile"] == "PDF/A-1B"


def test_convert_to_pdf_16_with_version_from_docx():
    resp = _convert_to_pdf_version(LibreOfficePdfProfile.PDF16)

    assert type(resp) is JSONResponse
    assert resp.status_code == 200
    json_resp = json.loads(resp.body)

    assert json_resp["compliant"] is False
    assert json_resp["profile"] == "PDF/A-1B"


"""
def test_convert_to_pdf_17_with_version_from_docx():
    resp = _convert_to_pdf_version(LibreOfficePdfProfile.PDF17)

    assert type(resp) is JSONResponse
    assert resp.status_code == 200
    json_resp = json.loads(resp.body)

    assert json_resp["compliant"] is False
    assert json_resp["profile"] == "PDF/A-1B"
"""


def test_convert_to_pdfa1_with_version_from_docx():
    resp = _convert_to_pdf_version(LibreOfficePdfProfile.PDFA1)

    assert type(resp) is JSONResponse
    assert resp.status_code == 200
    json_resp = json.loads(resp.body)

    assert json_resp["compliant"] is True
    assert json_resp["profile"] == "PDF/A-1A"


def test_convert_to_pdfa2_with_version_from_docx():
    resp = _convert_to_pdf_version(LibreOfficePdfProfile.PDFA2)

    assert type(resp) is JSONResponse
    assert resp.status_code == 200
    json_resp = json.loads(resp.body)

    assert json_resp["compliant"] is True
    assert json_resp["profile"] == "PDF/A-2B"


def test_convert_to_pdfa3_with_version_from_docx():
    resp = _convert_to_pdf_version(LibreOfficePdfProfile.PDFA3)

    assert type(resp) is JSONResponse
    assert resp.status_code == 200
    json_resp = json.loads(resp.body)

    assert json_resp["compliant"] is True
    assert json_resp["profile"] == "PDF/A-3B"


def _convert_to_pdf_version(pdf_version: LibreOfficePdfProfile) -> JSONResponse:
    converter = libreoffice.LibreOfficeAdapter()
    out = converter.convert_to_pdf(
        load_file("data/doc/normal_document.docx"), "test.docx", pdf_version
    )
    assert type(out) is FileResponse
    assert out.filename == "test.pdf"
    assert out.media_type == "application/pdf"
    converted_pdf = load_file(out.path)
    # simulate background thread
    assert os.path.exists(out.path) is True
    out.background.func(out.background.args[0])
    assert os.path.exists(out.path) is False
    # test if OCR worked
    extractor = pdf.PdfDataExtractor()
    txt_extracts = extractor.extract_text(converted_pdf, "test.pdf")
    assert len(txt_extracts) == 3
    assert len(txt_extracts[0].text) > 1000
    assert txt_extracts[1].page == 2
    assert len(txt_extracts[1].text) > 1000
    assert txt_extracts[2].page == 3
    assert len(txt_extracts[1].text) > 1000
    # validate
    validate = pdfa.PdfAValidator()
    resp = validate.validate_pdf(converted_pdf, "test.pdf")
    return resp
