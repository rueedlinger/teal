from starlette.testclient import TestClient

from teal import api
from tests import get_path


def test_pdf_ocr_extract_text_with_default_lang():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/ocr/scanned_document.pdf"), "rb") as f:
        response = client.post(url="/pdf/ocr", files={"file": f})
        assert response.status_code == 200
        assert len(response.json()) == 10
        for i in range(0, len(response.json())):
            assert response.json()[i]["page"] == i + 1
            assert len(response.json()[i]["text"]) > 1000


def test_pdf_ocr_extract_text_with_digital_pdf_with_default_lang():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/digital_pdf/document_two_pages.pdf"), "rb") as f:
        response = client.post(url="/pdf/ocr", files={"file": f})
        assert response.status_code == 200
        assert len(response.json()) == 2
        for i in range(0, len(response.json())):
            assert response.json()[i]["page"] == i + 1
            assert len(response.json()[i]["text"]) > 1000


def test_pdf_ocr_extract_text_with_lang_eng():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/ocr/scanned_document.pdf"), "rb") as f:
        response = client.post(url="/pdf/ocr?languages=eng", files={"file": f})
        assert response.status_code == 200
        assert len(response.json()) == 10
        for i in range(0, len(response.json())):
            assert response.json()[i]["page"] == i + 1
            assert len(response.json()[i]["text"]) > 1000


def test_pdf_ocr_extract_text_with_multi_lang():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/ocr/scanned_document.pdf"), "rb") as f:
        response = client.post(
            url="/pdf/ocr?languages=eng&languages=deu", files={"file": f}
        )
        assert response.status_code == 200
        assert len(response.json()) == 10
        for i in range(0, len(response.json())):
            assert response.json()[i]["page"] == i + 1
            assert len(response.json()[i]["text"]) > 1000


def test_pdf_ocr_extract_text_with_page_and_lang():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/ocr/scanned_document.pdf"), "rb") as f:
        response = client.post(url="/pdf/ocr?pages=2&languages=deu", files={"file": f})
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["page"] == 2
        assert len(response.json()[0]["text"]) > 1000


def test_pdf_ocr_extract_text_with_page_selection():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/ocr/scanned_document.pdf"), "rb") as f:
        response = client.post(url="/pdf/ocr?pages=2", files={"file": f})
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["page"] == 2
        assert len(response.json()[0]["text"]) > 1000


def test_pdf_ocr_extract_text_with_page_range():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/ocr/scanned_document.pdf"), "rb") as f:
        response = client.post(url="/pdf/ocr?pages=2-4", files={"file": f})
        assert response.status_code == 200
        assert len(response.json()) == 3
        assert response.json()[0]["page"] == 2
        assert len(response.json()[0]["text"]) > 1000
        assert response.json()[1]["page"] == 3
        assert len(response.json()[1]["text"]) > 1000
        assert response.json()[2]["page"] == 4
        assert len(response.json()[2]["text"]) > 1000


def test_pdf_ocr_extract_text_with_page_range_and_selection():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/ocr/scanned_document.pdf"), "rb") as f:
        response = client.post(url="/pdf/ocr?pages=1-2,4", files={"file": f})
        assert response.status_code == 200
        assert len(response.json()) == 3
        assert response.json()[0]["page"] == 1
        assert len(response.json()[0]["text"]) > 1000
        assert response.json()[1]["page"] == 2
        assert len(response.json()[1]["text"]) > 1000
        assert response.json()[2]["page"] == 4
        assert len(response.json()[2]["text"]) > 1000


def test_pdf_ocr_extract_text_with_wrong_file_ending():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/doc/word_document.docx"), "rb") as f:
        response = client.post(url="/pdf/ocr", files={"file": f})
        assert response.status_code == 400
        assert response.json() == {
            "message": "file extension '.docx' is not supported (word_document.docx)."
        }


def test_pdf_ocr_extract_text_with_wrong_languages():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/digital_pdf/document_two_pages.pdf"), "rb") as f:
        response = client.post(url="/pdf/ocr?languages=fooo", files={"file": f})
        assert response.status_code == 500
