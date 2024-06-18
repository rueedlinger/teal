import tempfile

import pytest
from starlette.testclient import TestClient

from teal import api
from teal.model.create import DocOutputType
from tests import get_path


@pytest.mark.parametrize(
    "file",
    ["data/digital_pdf/document_one_page.pdf", "data/ocr/scanned_document.pdf"],
)
def test_create_doc_with_default(file):
    client = TestClient(api.create_app(), raise_server_exceptions=False)
    with open(get_path(file), "rb") as f:
        response = client.post(url="/create/doc", files={"file": f})
        assert response.status_code == 200


@pytest.mark.parametrize(
    "file,output",
    [
        ("data/digital_pdf/document_one_page.pdf", DocOutputType.DOC),
        ("data/digital_pdf/document_one_page.pdf", DocOutputType.ODT),
        ("data/digital_pdf/document_one_page.pdf", DocOutputType.DOCX),
        ("data/ocr/scanned_document.pdf", DocOutputType.DOC),
        ("data/ocr/scanned_document.pdf", DocOutputType.ODT),
        ("data/ocr/scanned_document.pdf", DocOutputType.DOCX),
    ],
)
def test_create_doc_with_different_types(file, output):
    client = TestClient(api.create_app(), raise_server_exceptions=False)
    with open(get_path(file), "rb") as f:
        response = client.post(
            url=f"/create/doc?output={output.value}", files={"file": f}
        )
        assert response.status_code == 200


def test_create_doc_wrong_file_type():
    client = TestClient(api.app, raise_server_exceptions=False)
    with tempfile.NamedTemporaryFile(suffix=".xyz") as tmp:
        tmp.write(b"fff")
        response = client.post(url="/create/doc", files={"file": tmp})
        assert response.status_code == 400
        assert response.json() == {
            "message": "file extension '.xyz' is not supported, supported extensions are ['.doc', '.docx', '.odt', '.ott', '.pdf', '.rtf', '.text', '.txt']."
        }


def test_create_pdf_with_unsupported_param():
    client = TestClient(api.create_app(), raise_server_exceptions=False)
    with open(
        get_path("data/digital_pdf/document_with_multiple_tables.pdf"), "rb"
    ) as f:
        response = client.post(url=f"/create/doc?foo=ddd", files={"file": f})
        assert response.status_code == 400
        unknown_params = ["foo"]
        known_params = sorted(["output", "pages"])
        assert response.json() == {
            "message": f"Unknown request parameters: {unknown_params}, supported parameters are {known_params}"
        }
