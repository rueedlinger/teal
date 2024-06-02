import tempfile

from starlette.testclient import TestClient

from teal import api
from tests import get_path


def test_pdfa_convert_default():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/digital_pdf/normal_document.pdf"), "rb") as f:
        response = client.post(url="/pdfa/convert", files={"file": f})
        assert response.status_code == 200
        with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
            tmp.write(response.content)
            with open(tmp.name, "rb") as pdfa_file:
                response = client.post(url="/pdfa/validate", files={"file": pdfa_file})
                assert response.status_code == 200
                assert response.json()["compliant"] is True
                assert response.json()["profile"] == "PDF/A-1B"


def test_pdfa_convert_scanned_document_with_ocr():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/ocr/scanned_document.pdf"), "rb") as f:
        response = client.post(url="/pdfa/convert", files={"file": f})
        assert response.status_code == 200
        with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
            tmp.write(response.content)
            with open(tmp.name, "rb") as pdfa_file:
                response = client.post(url="/pdfa/validate", files={"file": pdfa_file})
                assert response.status_code == 200
                assert response.json()["compliant"] is True
                assert response.json()["profile"] == "PDF/A-1B"

                response = client.post(url="/pdf/text", files={"file": pdfa_file})
                assert response.status_code == 200
                assert len(response.json()) == 4


def test_pdfa_convert_with_lang():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/digital_pdf/normal_document.pdf"), "rb") as f:
        response = client.post(url="/pdfa/convert?languages=eng", files={"file": f})
        assert response.status_code == 200
        with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
            tmp.write(response.content)
            with open(tmp.name, "rb") as pdfa_file:
                response = client.post(url="/pdfa/validate", files={"file": pdfa_file})
                assert response.status_code == 200
                assert response.json()["compliant"] is True
                assert response.json()["profile"] == "PDF/A-1B"


def test_pdfa_convert_with_pages_selection():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/digital_pdf/normal_document.pdf"), "rb") as f:
        response = client.post(url="/pdfa/convert?pages=2", files={"file": f})
        assert response.status_code == 200
        with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
            tmp.write(response.content)
            with open(tmp.name, "rb") as pdfa_file:
                response = client.post(url="/pdfa/validate", files={"file": pdfa_file})
                assert response.status_code == 200
                assert response.json()["compliant"] is True
                assert response.json()["profile"] == "PDF/A-1B"

                response = client.post(url="/pdf/text", files={"file": pdfa_file})
                assert response.status_code == 200
                assert len(response.json()) == 1


def test_pdfa_convert_with_pages_range():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/digital_pdf/big_document.pdf"), "rb") as f:
        response = client.post(url="/pdfa/convert?pages=2-3", files={"file": f})
        assert response.status_code == 200
        with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
            tmp.write(response.content)
            with open(tmp.name, "rb") as pdfa_file:
                response = client.post(url="/pdfa/validate", files={"file": pdfa_file})
                assert response.status_code == 200
                assert response.json()["compliant"] is True
                assert response.json()["profile"] == "PDF/A-1B"

                response = client.post(url="/pdf/text", files={"file": pdfa_file})
                assert response.status_code == 200
                assert len(response.json()) == 2


def test_pdfa_convert_with_pages_range_and_selection():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/digital_pdf/big_document.pdf"), "rb") as f:
        response = client.post(url="/pdfa/convert?pages=2-3,8", files={"file": f})
        assert response.status_code == 200
        with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
            tmp.write(response.content)
            with open(tmp.name, "rb") as pdfa_file:
                response = client.post(url="/pdfa/validate", files={"file": pdfa_file})
                assert response.status_code == 200
                assert response.json()["compliant"] is True
                assert response.json()["profile"] == "PDF/A-1B"

                response = client.post(url="/pdf/text", files={"file": pdfa_file})
                assert response.status_code == 200
                assert len(response.json()) == 3


def test_pdfa_convert_to_pdfa1():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/digital_pdf/normal_document.pdf"), "rb") as f:
        response = client.post(url="/pdfa/convert?pdfa=pdfa-1b", files={"file": f})
        assert response.status_code == 200
        with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
            tmp.write(response.content)
            with open(tmp.name, "rb") as pdfa_file:
                response = client.post(url="/pdfa/validate", files={"file": pdfa_file})
                assert response.status_code == 200
                assert response.json()["compliant"] is True
                assert response.json()["profile"] == "PDF/A-1B"


def test_pdfa_convert_to_pdfa2():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/digital_pdf/normal_document.pdf"), "rb") as f:
        response = client.post(url="/pdfa/convert?pdfa=pdfa-2b", files={"file": f})
        assert response.status_code == 200
        with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
            tmp.write(response.content)
            with open(tmp.name, "rb") as pdfa_file:
                response = client.post(url="/pdfa/validate", files={"file": pdfa_file})
                assert response.status_code == 200
                assert response.json()["compliant"] is True
                assert response.json()["profile"] == "PDF/A-2B"


def test_pdfa_convert_to_pdfa3():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/digital_pdf/normal_document.pdf"), "rb") as f:
        response = client.post(url="/pdfa/convert?pdfa=pdfa-3b", files={"file": f})
        assert response.status_code == 200
        with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
            tmp.write(response.content)
            with open(tmp.name, "rb") as pdfa_file:
                response = client.post(url="/pdfa/validate", files={"file": pdfa_file})
                assert response.status_code == 200
                assert response.json()["compliant"] is True
                assert response.json()["profile"] == "PDF/A-3B"


def test_pdfa_convert_wrong_file_type():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/doc/normal_document.docx"), "rb") as f:
        response = client.post(url="/pdfa/convert", files={"file": f})
        assert response.status_code == 400
        assert response.json() == {
            "message": "file extension '.docx' is not supported (normal_document.docx)."
        }
