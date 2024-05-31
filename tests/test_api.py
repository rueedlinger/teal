from starlette.testclient import TestClient

import teal.api as api
from tests import get_path


def test_client():
    client = TestClient(api.app, raise_server_exceptions=False)
    response = client.get("/")
    assert response.status_code == 404


def test_pdf_text():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/digital_pdf/normal_document.pdf"), "rb") as f:
        response = client.post(url="/pdf/text", files={"file": f})
        assert response.status_code == 200
        assert len(response.json()) >= 1
        assert response.json()[0]["page"] == 1
        assert len(response.json()[0]["text"]) > 1000

    with open(get_path("data/digital_pdf/normal_document.pdf"), "rb") as f:
        response = client.post(url="/pdf/text?pages=2", files={"file": f})
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["page"] == 2
        assert len(response.json()[0]["text"]) > 1000

    with open(get_path("data/digital_pdf/big_document.pdf"), "rb") as f:
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


def test_pdf_ocr():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/ocr/scanned_document.pdf"), "rb") as f:
        response = client.post(url="/pdf/ocr", files={"file": f})
        assert response.status_code == 200
        assert len(response.json()) >= 1

    with open(get_path("data/ocr/scanned_document.pdf"), "rb") as f:
        response = client.post(url="/pdf/ocr?languages=eng&pages=2", files={"file": f})
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["page"] == 2
        assert len(response.json()[0]["text"]) > 1000

    with open(get_path("data/ocr/scanned_document.pdf"), "rb") as f:
        response = client.post(
            url="/pdf/ocr?languages=eng&pages=1-2", files={"file": f}
        )
        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json()[0]["page"] == 1
        assert len(response.json()[0]["text"]) > 1000
        assert response.json()[1]["page"] == 2
        assert len(response.json()[1]["text"]) > 1000

    with open(get_path("data/ocr/scanned_document.pdf"), "rb") as f:
        response = client.post(
            url="/pdf/ocr?languages=eng&pages=1,2", files={"file": f}
        )
        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json()[0]["page"] == 1
        assert len(response.json()[0]["text"]) > 1000
        assert response.json()[1]["page"] == 2
        assert len(response.json()[1]["text"]) > 1000

    with open(get_path("data/ocr/scanned_document.pdf"), "rb") as f:
        response = client.post(url="/pdf/ocr?languages=eng", files={"file": f})
        assert response.status_code == 200
        assert len(response.json()) >= 1
        assert response.json()[0]["page"] == 1
        assert len(response.json()[0]["text"]) > 1000

    with open(get_path("data/ocr/scanned_document.pdf"), "rb") as f:
        response = client.post(
            url="/pdf/ocr?languages=eng&languages=fra", files={"file": f}
        )
        assert response.status_code == 200
        assert len(response.json()) >= 1
        assert response.json()[0]["page"] == 1
        assert len(response.json()[0]["text"]) > 1000

    with open(get_path("data/ocr/scanned_document.pdf"), "rb") as f:
        response = client.post(url="/pdf/ocr?languages=foo", files={"file": f})
        assert response.status_code == 500


def test_pdf_table():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/digital_pdf/simple_tables.pdf"), "rb") as f:
        response = client.post(url="/pdf/table", files={"file": f})
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["page"] == 1
        assert response.json()[0]["index"] == 0
        assert len(response.json()[0]["table"]) >= 4

    with open(get_path("data/digital_pdf/multiple_tables.pdf"), "rb") as f:
        response = client.post(url="/pdf/table", files={"file": f})
        assert response.status_code == 200
        assert len(response.json()) == 3
        assert response.json()[0]["page"] == 1
        assert response.json()[0]["index"] == 0
        assert len(response.json()[0]["table"]) >= 4
        assert response.json()[1]["page"] == 1
        assert response.json()[1]["index"] == 1
        assert len(response.json()[1]["table"]) >= 4
        assert response.json()[2]["page"] == 2
        assert response.json()[2]["index"] == 0
        assert len(response.json()[2]["table"]) >= 4

    with open(get_path("data/digital_pdf/multiple_tables.pdf"), "rb") as f:
        response = client.post(url="/pdf/table?pages=1", files={"file": f})
        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json()[0]["page"] == 1
        assert response.json()[0]["index"] == 0
        assert len(response.json()[0]["table"]) >= 4
        assert response.json()[1]["page"] == 1
        assert response.json()[1]["index"] == 1
        assert len(response.json()[1]["table"]) >= 4


def test_pdfa_convert():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/digital_pdf/normal_document.pdf"), "rb") as f:
        response = client.post(url="/pdfa/convert", files={"file": f})
        assert response.status_code == 200


def test_pdfa_validate():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/pdfa/pdfa_2b.pdf"), "rb") as f:
        response = client.post(url="/pdfa/validate", files={"file": f})
        assert response.status_code == 200
        assert ("profile" in response.json()) is True


def test_libreoffice_convert():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/doc/normal_document.docx"), "rb") as f:
        response = client.post(url="/libreoffice/convert", files={"file": f})
        assert response.status_code == 200
