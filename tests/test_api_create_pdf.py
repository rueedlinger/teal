import tempfile

import pytest
from starlette.testclient import TestClient

from teal import api
from teal.model.create import OutputType
from tests import get_path


@pytest.mark.parametrize(
    "file",
    ["data/doc/text_document.txt", "data/doc/word_document.docx"],
)
def test_create_pdf_with_default(file):
    client = TestClient(api.create_app(), raise_server_exceptions=False)
    with open(get_path(file), "rb") as f:
        response = client.post(url="/create/pdf", files={"file": f})
        assert response.status_code == 200

        with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
            tmp.write(response.content)
            with open(tmp.name, "rb") as pdf_file:
                response = client.post(url="/extract/meta", files={"file": pdf_file})
                assert response.status_code == 200
                assert response.json()["pdfVersion"] == "1.7"
                assert response.json()["pdfaClaim"] is None


@pytest.mark.parametrize(
    "file,output,expected_version",
    [
        ("data/doc/text_document.txt", OutputType.PDF_15, "1.5"),
        ("data/doc/text_document.txt", OutputType.PDF_16, "1.6"),
        ("data/doc/text_document.txt", OutputType.PDF_17, "1.7"),
    ],
)
def test_create_pdf_with_output_pdf(file, output, expected_version):
    client = TestClient(api.create_app(), raise_server_exceptions=False)
    with open(get_path(file), "rb") as f:
        response = client.post(
            url=f"/create/pdf?output={output.value}", files={"file": f}
        )
        assert response.status_code == 200

        with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
            tmp.write(response.content)
            with open(tmp.name, "rb") as pdf_file:

                response = client.post(url="/extract/meta", files={"file": pdf_file})
                assert response.status_code == 200
                assert response.json()["pdfVersion"] == expected_version
                assert response.json()["pdfaClaim"] is None


@pytest.mark.parametrize(
    "file,output,expected_version,expected_pdfa",
    [
        ("data/doc/text_document.txt", OutputType.PDFA_1B, "1.4", "PDF/A-1B"),
        ("data/doc/text_document.txt", OutputType.PDFA_2B, "1.7", "PDF/A-2B"),
        ("data/doc/text_document.txt", OutputType.PDFA_3B, "1.7", "PDF/A-3B"),
    ],
)
def test_create_pdf_with_output_pdfa(file, output, expected_version, expected_pdfa):
    client = TestClient(api.create_app(), raise_server_exceptions=False)
    with open(get_path(file), "rb") as f:
        response = client.post(
            url=f"/create/pdf?output={output.value}", files={"file": f}
        )
        assert response.status_code == 200

        with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
            tmp.write(response.content)
            with open(tmp.name, "rb") as pdf_file:

                response = client.post(url="/extract/meta", files={"file": pdf_file})
                assert response.status_code == 200
                assert response.json()["pdfVersion"] == expected_version
                assert (
                    response.json()["pdfaClaim"]
                    == output.value.replace("pdfa-", "").upper()
                )

                response = client.post(
                    url=f"/validate/pdfa",
                    files={"file": pdf_file},
                )
                assert response.status_code == 200
                assert response.json()["compliant"] is True
                assert response.json()["profile"] == expected_pdfa


def test_create_pdf_wrong_file_type():
    client = TestClient(api.app, raise_server_exceptions=False)
    with tempfile.NamedTemporaryFile(suffix=".xyz") as tmp:
        tmp.write(b"fff")
        response = client.post(url="/create/pdf", files={"file": tmp})
        assert response.status_code == 400
        assert response.json() == {
            "message": "file extension '.xyz' is not supported, supported extensions are ['.doc', '.docx', '.odt', '.ott', '.pdf', '.rtf', '.text', '.txt']."
        }


def test_create_pdf_with_unsupported_param():
    client = TestClient(api.create_app(), raise_server_exceptions=False)
    with open(
        get_path("data/digital_pdf/document_with_multiple_tables.pdf"), "rb"
    ) as f:
        response = client.post(url=f"/create/pdf?foo=ddd", files={"file": f})
        assert response.status_code == 400
        unknown_params = ["foo"]
        known_params = sorted(["output", "pages"])
        assert response.json() == {
            "message": f"Unknown request parameters: {unknown_params}, supported parameters are {known_params}"
        }
