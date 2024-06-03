from starlette.testclient import TestClient

from teal import api
from tests import get_path


def test_pdf_extract_meta():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/digital_pdf/document_one_page.pdf"), "rb") as f:
        response = client.post(url="/pdf/meta", files={"file": f})
        assert response.status_code == 200
        assert response.json()["fileName"] == "document_one_page.pdf"
        assert response.json()["fileSize"] > 100
        assert response.json()["pdfVersion"] == "1.3"
        assert response.json()["pages"] == 1
        assert response.json()["pdfaClaim"] is None
        assert response.json()["docInfo"] is not None
        assert response.json()["xmp"] is not None


def test_pdf_extract_meta_with_wrong_file_ending():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/doc/word_document.docx"), "rb") as f:
        response = client.post(url="/pdf/text", files={"file": f})
        assert response.status_code == 400
        assert response.json() == {
            "message": "file extension '.docx' is not supported (word_document.docx)."
        }
