import os

from starlette.responses import FileResponse

import teal.pdf as pdf
from tests import load_file


def test_convert_pdf_from_digital_pdf():
    converter = pdf.PdfAConverter()
    out = converter.convert_pdf(load_file('data/digital_pdf/normal_document.pdf'), 'test.pdf')
    assert type(out) is FileResponse
    assert out.filename == 'test.pdf'
    assert out.media_type == 'application/pdf'
    pdfa = load_file(out.path)

    # simulate background thread
    assert os.path.exists(out.path) is True
    out.background.func(out.background.args[0])
    assert os.path.exists(out.path) is False

    # test if OCR worked
    extractor = pdf.PdfDataExtractor()
    txt_extracts = extractor.extract_text(pdfa, 'test.pdf')

    assert len(txt_extracts) == 2
    assert txt_extracts[0].page == 1
    assert len(txt_extracts[0].text) > 2000
    assert txt_extracts[1].page == 2
    assert len(txt_extracts[1].text) > 2000


def test_convert_pdf_from_scanned_pdf():
    converter = pdf.PdfAConverter()
    out = converter.convert_pdf(load_file('data/ocr/scanned_document.pdf'), 'test.pdf')
    assert type(out) is FileResponse
    assert out.filename == 'test.pdf'
    assert out.media_type == 'application/pdf'
    pdfa = load_file(out.path)

    # simulate background thread
    assert os.path.exists(out.path) is True
    out.background.func(out.background.args[0])
    assert os.path.exists(out.path) is False

    # test if OCR worked
    extractor = pdf.PdfDataExtractor()
    txt_extracts = extractor.extract_text(pdfa, 'test.pdf')

    assert len(txt_extracts) == 2
    assert txt_extracts[0].page == 1
    assert len(txt_extracts[0].text) > 2000
    assert txt_extracts[1].page == 2
    assert len(txt_extracts[1].text) > 2000


def test_convert_pdf_from_scanned_pdf_with_table():
    converter = pdf.PdfAConverter()
    out = converter.convert_pdf(load_file('data/ocr/scanned_document_with_table.pdf'), 'test.pdf')
    assert type(out) is FileResponse
    assert out.filename == 'test.pdf'
    assert out.media_type == 'application/pdf'
    pdfa = load_file(out.path)

    # simulate background thread
    assert os.path.exists(out.path) is True
    out.background.func(out.background.args[0])
    assert os.path.exists(out.path) is False

    # test if OCR worked
    extractor = pdf.PdfDataExtractor()
    table_extracts = extractor.extract_table(pdfa, 'test.pdf')

    assert len(table_extracts) == 1
    assert table_extracts[0].page == 1
    assert len(table_extracts[0].table) == 4
