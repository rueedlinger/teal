import teal.pdf as pdf
from tests import load_file


def test_extract_text():
    extractor = pdf.PdfDataExtractor()
    out = extractor.extract_text(load_file('data/digital_pdf/normal_document.pdf'), 'test.pdf')

    assert len(out) == 2
    assert out[0].page == 1
    assert len(out[0].text) > 2000
    assert out[1].page == 2
    assert len(out[1].text) > 2000


def test_extract_text_scanned_doc():
    extractor = pdf.PdfDataExtractor()
    out = extractor.extract_text(load_file('data/ocr/scanned_document.pdf'), 'test.pdf')

    assert len(out) == 2
    assert out[0].page == 1
    assert len(out[0].text) == 0
    assert out[1].page == 2
    assert len(out[1].text) == 0


def test_extract_text_small():
    extractor = pdf.PdfDataExtractor()
    out = extractor.extract_text(load_file('data/digital_pdf/small_document.pdf'), 'test.pdf')

    assert len(out) == 1
    assert out[0].page == 1
    assert len(out[0].text) == 22
    assert out[0].text == 'Test 1\r\nTest 2\r\nTest 3'


def test_extract_text_with_ocr_digital_pdf():
    extractor = pdf.PdfDataExtractor()
    out = extractor.extract_text_with_ocr(load_file('data/digital_pdf/normal_document.pdf'), 'test.pdf')

    assert len(out) == 2
    assert out[0].page == 1
    assert len(out[0].text) > 2000
    assert out[1].page == 2
    assert len(out[1].text) > 2000


def test_extract_text_with_ocr_scanned_pdf():
    extractor = pdf.PdfDataExtractor()
    out = extractor.extract_text_with_ocr(load_file('data/ocr/scanned_document.pdf'), 'test.pdf')

    assert len(out) == 2
    assert out[0].page == 1
    assert len(out[0].text) > 2000
    assert out[1].page == 2
    assert len(out[1].text) > 2000


def test_extract_text_with_ocr_small_digital_pdf():
    extractor = pdf.PdfDataExtractor()
    out = extractor.extract_text_with_ocr(load_file('data/digital_pdf/small_document.pdf'), 'test.pdf')

    assert len(out) == 1
    assert out[0].page == 1
    assert len(out[0].text) == 23
    assert out[0].text == 'Test 1\n\nTest 2\n\nTest 3\n'


def test_extract_tables():
    extractor = pdf.PdfDataExtractor()
    out = extractor.extract_table(load_file('data/digital_pdf/simple_tables.pdf'), 'test.pdf')
    assert len(out) == 1
    assert out[0].page == 1
    assert out[0].table == [{'0': 'A', '1': 'B', '2': 'C'}, {'0': 'A1', '1': 'B11', '2': 'C111'},
                            {'0': 'A2', '1': 'B22', '2': 'C222'}, {'0': 'A3', '1': 'B33', '2': 'C333'}]


def test_extract_when_no_tables():
    extractor = pdf.PdfDataExtractor()
    out = extractor.extract_table(load_file('data/digital_pdf/small_document.pdf'), 'test.pdf')
    assert len(out) == 0
