from teal.model.create import OutputType


def test_output_type_mapping():
    assert OutputType.PDFA_1B.to_param() == "1"
    assert OutputType.PDFA_2B.to_param() == "2"
    assert OutputType.PDFA_3B.to_param() == "3"
    assert OutputType.PDF_15.to_param() == "15"
    assert OutputType.PDF_16.to_param() == "16"
    assert OutputType.PDF_17.to_param() == "17"
