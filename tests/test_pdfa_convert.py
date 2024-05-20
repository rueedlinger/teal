import json
import os

from starlette.responses import FileResponse, JSONResponse

import teal.pdf as pdf
import teal.pdfa as pdfa
from tests import load_file


def test_non_zero_return_code():
    converter = pdfa.PdfAConverter()
    converter.ocrmypdf_cmd = 'foo'
    resp = converter.convert_pdfa(load_file('data/digital_pdf/normal_document.pdf'), 'test.pdf')
    assert type(resp) is JSONResponse
    assert resp.status_code == 500
    print(json.loads(resp.body))
    assert json.loads(resp.body) == {'message': "got return code 127 'test.pdf' /bin/sh: 1: foo: not found\n"}


def test_not_supported_types():
    converter = pdfa.PdfAConverter()
    resp = converter.convert_pdfa("", 'test.txt')
    assert type(resp) is JSONResponse
    assert resp.status_code == 400
    assert json.loads(resp.body) == {'message': "file extension '.txt' is not supported (test.txt)."}


def test_convert_pdf_from_digital_pdf():
    converter = pdfa.PdfAConverter()
    out = converter.convert_pdfa(load_file('data/digital_pdf/normal_document.pdf'), 'test.pdf')
    assert type(out) is FileResponse
    assert out.filename == 'test.pdf'
    assert out.media_type == 'application/pdf'
    pdfa_file = load_file(out.path)

    # simulate background thread
    assert os.path.exists(out.path) is True
    out.background.func(out.background.args[0])
    assert os.path.exists(out.path) is False

    # test if OCR worked
    extractor = pdf.PdfDataExtractor()
    txt_extracts = extractor.extract_text(pdfa_file, 'test.pdf')

    assert len(txt_extracts) == 2
    assert txt_extracts[0].page == 1
    assert len(txt_extracts[0].text) > 2000
    assert txt_extracts[1].page == 2
    assert len(txt_extracts[1].text) > 2000


def test_convert_pdf_from_scanned_pdf():
    converter = pdfa.PdfAConverter()
    out = converter.convert_pdfa(load_file('data/ocr/scanned_document.pdf'), 'test.pdf')
    assert type(out) is FileResponse
    assert out.filename == 'test.pdf'
    assert out.media_type == 'application/pdf'
    pdfa_file = load_file(out.path)

    # simulate background thread
    assert os.path.exists(out.path) is True
    out.background.func(out.background.args[0])
    assert os.path.exists(out.path) is False

    # test if OCR worked
    extractor = pdf.PdfDataExtractor()
    txt_extracts = extractor.extract_text(pdfa_file, 'test.pdf')

    assert len(txt_extracts) == 2
    assert txt_extracts[0].page == 1
    assert len(txt_extracts[0].text) > 2000
    assert txt_extracts[1].page == 2
    assert len(txt_extracts[1].text) > 2000


def test_convert_pdf_from_scanned_pdf_with_table():
    converter = pdfa.PdfAConverter()
    out = converter.convert_pdfa(load_file('data/ocr/scanned_document_with_table.pdf'), 'test.pdf')
    assert type(out) is FileResponse
    assert out.filename == 'test.pdf'
    assert out.media_type == 'application/pdf'
    pdfa_file = load_file(out.path)

    # simulate background thread
    assert os.path.exists(out.path) is True
    out.background.func(out.background.args[0])
    assert os.path.exists(out.path) is False

    # test if OCR worked
    extractor = pdf.PdfDataExtractor()
    table_extracts = extractor.extract_table(pdfa_file, 'test.pdf')

    assert len(table_extracts) == 1
    assert table_extracts[0].page == 1
    assert len(table_extracts[0].table) == 4


def test_validate_pdfa_success():
    converter = pdfa.PdfAConverter()
    out = converter.convert_pdfa(load_file('data/ocr/scanned_document_with_table.pdf'), 'test.pdf')
    assert type(out) is FileResponse
    assert out.filename == 'test.pdf'
    assert out.media_type == 'application/pdf'
    pdfa_file = load_file(out.path)

    # simulate background thread
    assert os.path.exists(out.path) is True
    out.background.func(out.background.args[0])
    assert os.path.exists(out.path) is False

    validator = pdfa.PdfAValidator()
    resp = validator.validate_pdf(pdfa_file, filename='test.pdf')

    assert type(resp) is JSONResponse
    assert resp.status_code == 200
    json_resp = json.loads(resp.body)

    assert json_resp['compliant'] is True
    assert json_resp['profile'] == 'PDF/A-2B'

    # simulate background thread
    assert os.path.exists(resp.background.args[0]) is True
    resp.background.func(resp.background.args[0])
    assert os.path.exists(resp.background.args[0]) is False


def test_validate_pdfa_failed():
    validator = pdfa.PdfAValidator()
    resp = validator.validate_pdf(load_file('data/ocr/scanned_document_with_table.pdf'), filename='test.pdf')

    assert type(resp) is JSONResponse
    assert resp.status_code == 200
    json_resp = json.loads(resp.body)

    assert json_resp['compliant'] is False
    assert json_resp['profile'] == 'PDF/A-1B'
