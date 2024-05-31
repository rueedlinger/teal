import json

from starlette.responses import JSONResponse

import teal.pdf as pdf
from tests import load_file


def test_not_supported_types():
    extractor = pdf.PdfDataExtractor()
    resp = extractor.extract_text("", "test.txt")
    assert type(resp) is JSONResponse
    assert resp.status_code == 400
    assert json.loads(resp.body) == {
        "message": "file extension '.txt' is not supported (test.txt)."
    }

    resp = extractor.extract_table("", "test.txt")
    assert type(resp) is JSONResponse
    assert resp.status_code == 400
    assert json.loads(resp.body) == {
        "message": "file extension '.txt' is not supported (test.txt)."
    }

    resp = extractor.extract_text_with_ocr("", "test.txt")
    assert type(resp) is JSONResponse
    assert resp.status_code == 400
    assert json.loads(resp.body) == {
        "message": "file extension '.txt' is not supported (test.txt)."
    }


def test_extract_text_from_digital_pdf():
    extractor = pdf.PdfDataExtractor()
    txt_extracts = extractor.extract_text(
        load_file("data/digital_pdf/normal_document.pdf"), "test.pdf"
    )

    assert len(txt_extracts) == 2
    assert txt_extracts[0].page == 1
    assert len(txt_extracts[0].text) > 2000
    assert txt_extracts[1].page == 2
    assert len(txt_extracts[1].text) > 2000


def test_extract_text_from_scanned_pdf():
    extractor = pdf.PdfDataExtractor()
    txt_extracts = extractor.extract_text(
        load_file("data/ocr/scanned_document.pdf"), "test.pdf"
    )

    assert len(txt_extracts) == 2
    assert txt_extracts[0].page == 1
    assert len(txt_extracts[0].text) == 0
    assert txt_extracts[1].page == 2
    assert len(txt_extracts[1].text) == 0


def test_extract_text_small_from_digital_pdf():
    extractor = pdf.PdfDataExtractor()
    txt_extracts = extractor.extract_text(
        load_file("data/digital_pdf/small_document.pdf"), "test.pdf"
    )

    assert len(txt_extracts) == 1
    assert txt_extracts[0].page == 1
    assert len(txt_extracts[0].text) == 22
    assert txt_extracts[0].text == "Test 1\r\nTest 2\r\nTest 3"


def test_extract_text_with_ocr_from_digital_pdf():
    extractor = pdf.PdfDataExtractor()
    txt_extracts = extractor.extract_text_with_ocr(
        load_file("data/digital_pdf/normal_document.pdf"), "test.pdf"
    )

    assert len(txt_extracts) == 2
    assert txt_extracts[0].page == 1
    assert len(txt_extracts[0].text) > 2000
    assert txt_extracts[1].page == 2
    assert len(txt_extracts[1].text) > 2000


def test_extract_text_small_with_ocr_from_digital_pdf():
    extractor = pdf.PdfDataExtractor()
    txt_extracts = extractor.extract_text_with_ocr(
        load_file("data/digital_pdf/small_document.pdf"), "test.pdf"
    )

    assert len(txt_extracts) == 1
    assert txt_extracts[0].page == 1
    assert len(txt_extracts[0].text) == 23
    assert txt_extracts[0].text == "Test 1\n\nTest 2\n\nTest 3\n"


def test_extract_text_with_ocr_from_scanned_pdf():
    extractor = pdf.PdfDataExtractor()
    txt_extracts = extractor.extract_text_with_ocr(
        load_file("data/ocr/scanned_document.pdf"), "test.pdf"
    )

    assert len(txt_extracts) == 2
    assert txt_extracts[0].page == 1
    assert len(txt_extracts[0].text) > 2000
    assert txt_extracts[1].page == 2
    assert len(txt_extracts[1].text) > 2000


def test_extract_tables_from_digital_pdf_with_tables():
    extractor = pdf.PdfDataExtractor()
    table_extracts = extractor.extract_table(
        load_file("data/digital_pdf/simple_tables.pdf"), "test.pdf"
    )
    assert len(table_extracts) == 1
    assert table_extracts[0].page == 1
    assert table_extracts[0].index == 0
    assert table_extracts[0].table == [
        {"0": "A", "1": "B", "2": "C"},
        {"0": "A1", "1": "B11", "2": "C111"},
        {"0": "A2", "1": "B22", "2": "C222"},
        {"0": "A3", "1": "B33", "2": "C333"},
    ]


def test_extract_multiple_tables_from_digital_pdf_with_tables():
    extractor = pdf.PdfDataExtractor()
    table_extracts = extractor.extract_table(
        load_file("data/digital_pdf/multiple_tables.pdf"), "test.pdf"
    )
    assert len(table_extracts) == 3
    assert table_extracts[0].page == 1
    assert table_extracts[0].index == 0
    assert table_extracts[0].table == [
        {"0": "A", "1": "B", "2": "C", "3": "D"},
        {"0": "A1", "1": "B1", "2": "C1", "3": "D1"},
        {"0": "A2", "1": "B2", "2": "C2", "3": "D2"},
        {"0": "A3", "1": "B3", "2": "C3", "3": "D3"},
        {"0": "A4", "1": "B4", "2": "C4", "3": "D4"},
    ]

    assert table_extracts[1].page == 1
    assert table_extracts[1].index == 1
    assert table_extracts[1].table == [
        {"0": "AA", "1": "BB", "2": "CC", "3": "DD"},
        {"0": "AA1", "1": "BB1", "2": "CC1", "3": "DD1"},
        {"0": "AA2", "1": "BB2", "2": "CC2", "3": "DD2"},
        {"0": "AA3", "1": "BB3", "2": "CC3", "3": "DD3"},
        {"0": "AA4", "1": "BB4", "2": "CC4", "3": "DD4"},
    ]

    assert table_extracts[2].page == 2
    assert table_extracts[2].index == 0
    assert table_extracts[2].table == [
        {"0": "X", "1": "Y"},
        {"0": "X1", "1": "Y1"},
        {"0": "X2", "1": "Y2"},
        {"0": "X3", "1": "Y3"},
        {"0": "X4", "1": "Y4"},
    ]


def test_no_extract_tables_from_scanned_pdf_with_tables():
    extractor = pdf.PdfDataExtractor()
    table_extracts = extractor.extract_table(
        load_file("data/ocr/scanned_document_with_table.pdf"), "test.pdf"
    )
    assert len(table_extracts) == 0


def test_no_extract_tables_from_digital_pdf_with_no_tables():
    extractor = pdf.PdfDataExtractor()
    table_extracts = extractor.extract_table(
        load_file("data/digital_pdf/small_document.pdf"), "test.pdf"
    )
    assert len(table_extracts) == 0
