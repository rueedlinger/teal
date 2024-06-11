import tempfile

import pytest
from starlette.testclient import TestClient

from teal import api
from teal.model.validate import ValidatePdfProfile
from tests import get_path


def test_validate_pdfa_compliant_pdfa():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/pdfa/pdfa_2b.pdf"), "rb") as f:
        response = client.post(url="/validate/pdfa", files={"file": f})
        assert response.status_code == 200
        assert response.json()["compliant"] is True
        assert response.json()["profile"] == "PDF/A-2B"


def test_validate_pdfa_non_compliant_pdfa():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/digital_pdf/document_two_pages.pdf"), "rb") as f:
        response = client.post(url="/validate/pdfa", files={"file": f})
        assert response.status_code == 200
        assert response.json()["compliant"] is False
        assert response.json()["profile"] == "NONE"


@pytest.mark.parametrize(
    "profile_param, expected_profile",
    [
        (ValidatePdfProfile.PDFA_1A, "PDF/A-1A"),
        (ValidatePdfProfile.PDFA_1B, "PDF/A-1B"),
        (ValidatePdfProfile.PDFA_2A, "PDF/A-2A"),
        (ValidatePdfProfile.PDFA_2B, "PDF/A-2B"),
        (ValidatePdfProfile.PDFA_3B, "PDF/A-3B"),
        (ValidatePdfProfile.PDFA_3A, "PDF/A-3A"),
        (ValidatePdfProfile.PDFA_3U, "PDF/A-3U"),
        (ValidatePdfProfile.PDFA_4, "PDF/A-4"),
        (ValidatePdfProfile.PDFA_4f, "PDF/A-4F"),
        (ValidatePdfProfile.PDFA_4e, "PDF/A-4E"),
        (ValidatePdfProfile.PDFUA_1, "PDF/UA-1"),
        (ValidatePdfProfile.PDFUA_2, "PDF/UA-2"),
    ],
)
def test_validate_pdfa_all_profile_non_compliant_pdfa(profile_param, expected_profile):
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/digital_pdf/document_two_pages.pdf"), "rb") as f:
        response = client.post(
            url=f"/validate/pdfa?profile={profile_param.value}", files={"file": f}
        )
        assert response.status_code == 200
        assert response.json()["compliant"] is False
        assert response.json()["profile"] == expected_profile


def test_validate_pdfa_with_wrong_file_ending():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/doc/word_document.docx"), "rb") as f:
        response = client.post(url="/validate/pdfa", files={"file": f})
        assert response.status_code == 400
        assert response.json() == {
            "message": f"file extension '.docx' is not supported (word_document.docx)."
        }


def test_validate_pdfa_with_unsupported_param():
    client = TestClient(api.create_app(), raise_server_exceptions=False)
    with open(get_path("data/digital_pdf/document_two_pages.pdf"), "rb") as f:
        response = client.post(url=f"/validate/pdfa?foo=ddd", files={"file": f})
        assert response.status_code == 400
        unknown_params = ["foo"]
        known_params = ["profile"]
        assert response.json() == {
            "message": f"Unknown request parameters: {unknown_params}, supported parameters are {known_params}"
        }


def test_validate_pdfa_meta_corrupt_file():
    client = TestClient(api.app, raise_server_exceptions=False)
    with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
        tmp.write(b"fff")
        response = client.post(url="/validate/pdfa", files={"file": tmp})
        assert response.status_code == 500
