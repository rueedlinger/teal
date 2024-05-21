from starlette.testclient import TestClient

import teal.api as api
from tests import get_path


def test_client():
    client = TestClient(api.app)
    response = client.get("/")
    assert response.status_code == 404


def test_pdf_text():
    client = TestClient(api.app)
    with open(get_path("data/digital_pdf/normal_document.pdf"), "rb") as f:
        response = client.post(url="/pdf/text", files={"file": f})
        assert response.status_code == 200
        assert len(response.json()) >= 1


def test_pdf_ocr():
    client = TestClient(api.app)
    with open(get_path("data/ocr/scanned_document.pdf"), "rb") as f:
        response = client.post(url="/pdf/ocr", files={"file": f})
        assert response.status_code == 200
        assert len(response.json()) >= 1


def test_pdf_table():
    client = TestClient(api.app)
    with open(get_path("data/digital_pdf/simple_tables.pdf"), "rb") as f:
        response = client.post(url="/pdf/ocr", files={"file": f})
        assert response.status_code == 200
        assert len(response.json()) >= 1


def test_pdfa_convert():
    client = TestClient(api.app)
    with open(get_path("data/digital_pdf/normal_document.pdf"), "rb") as f:
        response = client.post(url="/pdfa/convert", files={"file": f})
        assert response.status_code == 200


def test_pdfa_validate():
    client = TestClient(api.app)
    with open(get_path("data/pdfa/pdfa_2b.pdf"), "rb") as f:
        response = client.post(url="/pdfa/validate", files={"file": f})
        assert response.status_code == 200
        assert ("profile" in response.json()) is True


def test_libreoffice_convert():
    client = TestClient(api.app)
    with open(get_path("data/doc/normal_document.docx"), "rb") as f:
        response = client.post(url="/libreoffice/convert", files={"file": f})
        assert response.status_code == 200
