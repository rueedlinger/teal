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


def test_extract_text_with_ocr_small_digital_pdf():
    extractor = pdf.PdfDataExtractor()
    out = extractor.extract_text_with_ocr(load_file('data/digital_pdf/small_document.pdf'), 'test.pdf')

    assert len(out) == 1
    assert out[0].page == 1
    assert len(out[0].text) == 23
    assert out[0].text == 'Test 1\n\nTest 2\n\nTest 3\n'


def test_extract_tables():
    extractor = pdf.PdfDataExtractor()
    out = extractor.extract_table(load_file('data/digital_pdf/small_document.pdf'), 'test.pdf')
    assert len(out) == 0
