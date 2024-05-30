from teal.model import LibreOfficePdfProfile


def test_libreoffice_model():
    # assert LibreOfficePdfProfile.PDF17.to_libreoffice_pdf_version() == "17"
    assert LibreOfficePdfProfile.PDF16.to_libreoffice_pdf_version() == "16"
    assert LibreOfficePdfProfile.PDF15.to_libreoffice_pdf_version() == "15"
    assert LibreOfficePdfProfile.PDFA1.to_libreoffice_pdf_version() == "1"
    assert LibreOfficePdfProfile.PDFA2.to_libreoffice_pdf_version() == "2"
    assert LibreOfficePdfProfile.PDFA3.to_libreoffice_pdf_version() == "3"
