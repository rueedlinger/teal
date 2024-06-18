from teal.model.create import PdfOutputType, DocOutputType


def test_output_type_mapping():
    assert PdfOutputType.PDFA_1B.to_param() == "1"
    assert PdfOutputType.PDFA_2B.to_param() == "2"
    assert PdfOutputType.PDFA_3B.to_param() == "3"
    assert PdfOutputType.PDF_15.to_param() == "15"
    assert PdfOutputType.PDF_16.to_param() == "16"
    assert PdfOutputType.PDF_17.to_param() == "17"


def test_doc_file_ext():
    assert DocOutputType.DOC.to_file_ext() == ".doc"
    assert DocOutputType.DOCX.to_file_ext() == ".docx"
    assert DocOutputType.ODT.to_file_ext() == ".odt"
