import teal.pdf as pdf
from tests import load_file


def test_extract_text_from_digital_pdf():
    extractor = pdf.PdfDataExtractor()
    txt_extracts = extractor.extract_text(load_file('data/digital_pdf/normal_document.pdf'), 'test.pdf')

    assert len(txt_extracts) == 2
    assert txt_extracts[0].page == 1
    assert len(txt_extracts[0].text) > 2000
    assert txt_extracts[1].page == 2
    assert len(txt_extracts[1].text) > 2000


def test_extract_text_from_scanned_pdf():
    extractor = pdf.PdfDataExtractor()
    txt_extracts = extractor.extract_text(load_file('data/ocr/scanned_document.pdf'), 'test.pdf')

    assert len(txt_extracts) == 2
    assert txt_extracts[0].page == 1
    assert len(txt_extracts[0].text) == 0
    assert txt_extracts[1].page == 2
    assert len(txt_extracts[1].text) == 0


def test_extract_text_small_from_digital_pdf():
    extractor = pdf.PdfDataExtractor()
    txt_extracts = extractor.extract_text(load_file('data/digital_pdf/small_document.pdf'), 'test.pdf')

    assert len(txt_extracts) == 1
    assert txt_extracts[0].page == 1
    assert len(txt_extracts[0].text) == 22
    assert txt_extracts[0].text == 'Test 1\r\nTest 2\r\nTest 3'


def test_extract_text_with_ocr_from_digital_pdf():
    extractor = pdf.PdfDataExtractor()
    txt_extracts = extractor.extract_text_with_ocr(load_file('data/digital_pdf/normal_document.pdf'), 'test.pdf')

    assert len(txt_extracts) == 2
    assert txt_extracts[0].page == 1
    assert len(txt_extracts[0].text) > 2000
    assert txt_extracts[1].page == 2
    assert len(txt_extracts[1].text) > 2000


def test_extract_text_small_with_ocr_from_digital_pdf():
    extractor = pdf.PdfDataExtractor()
    txt_extracts = extractor.extract_text_with_ocr(load_file('data/digital_pdf/small_document.pdf'), 'test.pdf')

    assert len(txt_extracts) == 1
    assert txt_extracts[0].page == 1
    assert len(txt_extracts[0].text) == 23
    assert txt_extracts[0].text == 'Test 1\n\nTest 2\n\nTest 3\n'


def test_extract_text_with_ocr_from_scanned_pdf():
    extractor = pdf.PdfDataExtractor()
    txt_extracts = extractor.extract_text_with_ocr(load_file('data/ocr/scanned_document.pdf'), 'test.pdf')

    assert len(txt_extracts) == 2
    assert txt_extracts[0].page == 1
    assert len(txt_extracts[0].text) > 2000
    assert txt_extracts[1].page == 2
    assert len(txt_extracts[1].text) > 2000


def test_extract_tables_from_digital_pdf_with_tables():
    extractor = pdf.PdfDataExtractor()
    table_extracts = extractor.extract_table(load_file('data/digital_pdf/simple_tables.pdf'), 'test.pdf')
    assert len(table_extracts) == 1
    assert table_extracts[0].page == 1
    assert table_extracts[0].table == [{'0': 'A', '1': 'B', '2': 'C'}, {'0': 'A1', '1': 'B11', '2': 'C111'},
                                       {'0': 'A2', '1': 'B22', '2': 'C222'}, {'0': 'A3', '1': 'B33', '2': 'C333'}]


def test_no_extract_tables_from_scanned_pdf_with_tables():
    extractor = pdf.PdfDataExtractor()
    table_extracts = extractor.extract_table(load_file('data/ocr/scanned_document_with_table.pdf'), 'test.pdf')
    assert len(table_extracts) == 0


def test_no_extract_tables_from_digital_pdf_with_no_tables():
    extractor = pdf.PdfDataExtractor()
    table_extracts = extractor.extract_table(load_file('data/digital_pdf/small_document.pdf'), 'test.pdf')
    assert len(table_extracts) == 0
