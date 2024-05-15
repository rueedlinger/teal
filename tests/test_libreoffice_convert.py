import json
import os

from starlette.responses import FileResponse, JSONResponse

import teal.libreoffice as libreoffice
import teal.pdf as pdf
from tests import load_file


def test_not_supported_types():
    converter = libreoffice.LibreOfficeAdapter()
    resp = converter.convert_to_pdf("", 'test.zip')
    assert type(resp) is JSONResponse
    assert resp.status_code == 400
    assert json.loads(resp.body) == {'message': "file extension '.zip' is not supported (test.zip)."}


def test_convert_to_pdf_from_docx():
    converter = libreoffice.LibreOfficeAdapter()
    out = converter.convert_to_pdf(load_file('data/doc/normal_document.docx'), 'test.docx')
    assert type(out) is FileResponse
    assert out.filename == 'test.pdf'
    assert out.media_type == 'application/pdf'
    converted_pdf = load_file(out.path)

    # simulate background thread
    assert os.path.exists(out.path) is True
    out.background.func(out.background.args[0])
    assert os.path.exists(out.path) is False

    # test if OCR worked
    extractor = pdf.PdfDataExtractor()
    txt_extracts = extractor.extract_text(converted_pdf, 'test.pdf')

    assert len(txt_extracts) == 3
    assert len(txt_extracts[0].text) > 1000
    assert txt_extracts[1].page == 2
    assert len(txt_extracts[1].text) > 1000
    assert txt_extracts[2].page == 3
    assert len(txt_extracts[1].text) > 1000
