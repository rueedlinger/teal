from teal.model.ocr import OutputType, OcrMode


def test_output_type_mapping():
    assert OutputType.PDFA_1B.to_param() == "pdfa-1"
    assert OutputType.PDFA_2B.to_param() == "pdfa-2"
    assert OutputType.PDFA_3B.to_param() == "pdfa-3"
    assert OutputType.PDF.to_param() == "pdf"


def test_ocr_mode_mapping():
    assert OcrMode.SKIP_TEXT.to_param() == "--skip-text"
    assert OcrMode.FORCE_OCR.to_param() == "--force-ocr"
    assert OcrMode.REDO_OCR.to_param() == "--redo-ocr"
