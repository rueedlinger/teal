from starlette.testclient import TestClient

from teal import api
from tests import get_path


def test_pdf_extract_text():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/digital_pdf/document_two_pages.pdf"), "rb") as f:
        response = client.post(url="/pdf/text", files={"file": f})
        assert response.status_code == 200
        assert len(response.json()) >= 1
        assert response.json()[0]["page"] == 1
        assert len(response.json()[0]["text"]) > 1000


def test_pdf_extract_text_with_page_selection():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/digital_pdf/document_two_pages.pdf"), "rb") as f:
        response = client.post(url="/pdf/text?pages=2", files={"file": f})
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["page"] == 2
        assert len(response.json()[0]["text"]) > 1000


def test_pdf_extract_text_with_page_range():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/digital_pdf/document_multiple_pages.pdf"), "rb") as f:
        response = client.post(url="/pdf/text?pages=2-5", files={"file": f})
        assert response.status_code == 200
        assert len(response.json()) == 4
        assert response.json()[0]["page"] == 2
        assert len(response.json()[0]["text"]) > 1000
        assert response.json()[1]["page"] == 3
        assert len(response.json()[1]["text"]) > 1000
        assert response.json()[2]["page"] == 4
        assert len(response.json()[2]["text"]) > 1000
        assert response.json()[3]["page"] == 5
        assert len(response.json()[3]["text"]) > 1000


def test_pdf_extract_text_with_page_range_and_selection():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/digital_pdf/document_multiple_pages.pdf"), "rb") as f:
        response = client.post(url="/pdf/text?pages=2-5,9", files={"file": f})
        assert response.status_code == 200
        assert len(response.json()) == 5
        assert response.json()[0]["page"] == 2
        assert len(response.json()[0]["text"]) > 1000
        assert response.json()[1]["page"] == 3
        assert len(response.json()[1]["text"]) > 1000
        assert response.json()[2]["page"] == 4
        assert len(response.json()[2]["text"]) > 1000
        assert response.json()[3]["page"] == 5
        assert len(response.json()[3]["text"]) > 1000
        assert response.json()[4]["page"] == 9
        assert len(response.json()[4]["text"]) > 1000


def test_pdf_extract_text_with_wrong_file_ending():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/doc/word_document.docx"), "rb") as f:
        response = client.post(url="/pdf/text", files={"file": f})
        assert response.status_code == 400
        assert response.json() == {
            "message": "file extension '.docx' is not supported (word_document.docx)."
        }
