from teal.model import LibreOfficePdfProfile, OcrPdfAProfile


def test_libreoffice_pdf_profile_model():
    # assert LibreOfficePdfProfile.PDF17.to_libreoffice_pdf_version() == "17"
    assert LibreOfficePdfProfile.PDF_16.to_libreoffice_pdf_version() == "16"
    assert LibreOfficePdfProfile.PDF_15.to_libreoffice_pdf_version() == "15"
    assert LibreOfficePdfProfile.PDFA_1a.to_libreoffice_pdf_version() == "1"
    assert LibreOfficePdfProfile.PDFA_2B.to_libreoffice_pdf_version() == "2"
    assert LibreOfficePdfProfile.PDFA_3B.to_libreoffice_pdf_version() == "3"


def test_ocr_pdf_profile_model():
    assert OcrPdfAProfile.PDFA_1B.to_ocrmypdf_profile() == "pdfa-1"
    assert OcrPdfAProfile.PDFA_2B.to_ocrmypdf_profile() == "pdfa-2"
    assert OcrPdfAProfile.PDFA_3B.to_ocrmypdf_profile() == "pdfa-3"
