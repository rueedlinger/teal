import os
import tempfile

from starlette.testclient import TestClient

from teal import api
from tests import get_path


def test_libreoffice_convert_docx_default():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/doc/word_document.docx"), "rb") as f:
        response = client.post(url="/libreoffice/convert", files={"file": f})
        assert response.status_code == 200
        with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
            tmp.write(response.content)
            with open(tmp.name, "rb") as pdf_file:
                response = client.post(url="/pdf/text", files={"file": pdf_file})
                assert response.status_code == 200
                assert len(response.json()) == 3

                response = client.post(url="/pdf/meta", files={"file": pdf_file})
                assert response.status_code == 200
                assert response.json()["pdfVersion"] == "1.7"
                assert response.json()["pdfaClaim"] is None


def test_libreoffice_convert_docx_pdf15():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/doc/word_document.docx"), "rb") as f:
        response = client.post(
            url="/libreoffice/convert?profile=pdf-1.5", files={"file": f}
        )
        assert response.status_code == 200
        with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
            tmp.write(response.content)
            with open(tmp.name, "rb") as pdf_file:
                response = client.post(url="/pdf/text", files={"file": pdf_file})
                assert response.status_code == 200
                assert len(response.json()) == 3

                response = client.post(url="/pdf/meta", files={"file": pdf_file})
                assert response.status_code == 200
                assert response.json()["pdfVersion"] == "1.5"
                assert response.json()["pdfaClaim"] is None


def test_libreoffice_convert_docx_pdf16():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/doc/word_document.docx"), "rb") as f:
        response = client.post(
            url="/libreoffice/convert?profile=pdf-1.6", files={"file": f}
        )
        assert response.status_code == 200
        with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
            tmp.write(response.content)
            with open(tmp.name, "rb") as pdf_file:
                response = client.post(url="/pdf/text", files={"file": pdf_file})
                assert response.status_code == 200
                assert len(response.json()) == 3

                response = client.post(url="/pdf/meta", files={"file": pdf_file})
                assert response.status_code == 200
                assert response.json()["pdfVersion"] == "1.6"
                assert response.json()["pdfaClaim"] is None


def test_libreoffice_convert_docx_pdf17():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/doc/word_document.docx"), "rb") as f:
        response = client.post(
            url="/libreoffice/convert?profile=pdf-1.7", files={"file": f}
        )
        assert response.status_code == 200
        with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
            tmp.write(response.content)
            with open(tmp.name, "rb") as pdf_file:
                response = client.post(url="/pdf/text", files={"file": pdf_file})
                assert response.status_code == 200
                assert len(response.json()) == 3

                response = client.post(url="/pdf/meta", files={"file": pdf_file})
                assert response.status_code == 200
                assert response.json()["pdfVersion"] == "1.7"
                assert response.json()["pdfaClaim"] is None


def test_libreoffice_convert_txt_default():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/doc/text_document.txt"), "rb") as f:
        response = client.post(url="/libreoffice/convert", files={"file": f})
        assert response.status_code == 200
        with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
            tmp.write(response.content)
            with open(tmp.name, "rb") as pdf_file:
                response = client.post(url="/pdf/text", files={"file": pdf_file})
                assert response.status_code == 200
                assert len(response.json()) == 1

                response = client.post(url="/pdf/meta", files={"file": pdf_file})
                assert response.status_code == 200
                assert response.json()["pdfVersion"] == "1.7"
                assert response.json()["pdfaClaim"] is None


def test_libreoffice_convert_pdf_default():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/digital_pdf/document_two_pages.pdf"), "rb") as f:
        response = client.post(url="/libreoffice/convert", files={"file": f})
        assert response.status_code == 200
        with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
            tmp.write(response.content)
            with open(tmp.name, "rb") as pdf_file:
                response = client.post(url="/pdf/text", files={"file": pdf_file})
                assert response.status_code == 200
                assert len(response.json()) == 2

                response = client.post(url="/pdf/meta", files={"file": pdf_file})
                assert response.status_code == 200
                assert response.json()["pdfVersion"] == "1.7"
                assert response.json()["pdfaClaim"] is None


def test_libreoffice_convert_with_selection():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/doc/word_document.docx"), "rb") as f:
        response = client.post(url="/libreoffice/convert?pages=1", files={"file": f})
        assert response.status_code == 200
        with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
            tmp.write(response.content)
            with open(tmp.name, "rb") as pdf_file:
                response = client.post(url="/pdf/text", files={"file": pdf_file})
                assert response.status_code == 200
                assert len(response.json()) == 1


def test_libreoffice_convert_with_page_range():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/doc/word_document.docx"), "rb") as f:
        response = client.post(url="/libreoffice/convert?pages=2-3", files={"file": f})
        assert response.status_code == 200
        with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
            tmp.write(response.content)
            with open(tmp.name, "rb") as pdf_file:
                response = client.post(url="/pdf/text", files={"file": pdf_file})
                assert response.status_code == 200
                assert len(response.json()) == 2


def test_libreoffice_convert_pdfa1():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/doc/word_document.docx"), "rb") as f:
        response = client.post(
            url="/libreoffice/convert?profile=pdfa-1b", files={"file": f}
        )
        assert response.status_code == 200
        with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
            tmp.write(response.content)
            with open(tmp.name, "rb") as pdf_file:
                response = client.post(url="/pdfa/validate", files={"file": pdf_file})
                assert response.status_code == 200
                assert response.json()["compliant"] is True
                assert response.json()["profile"] == "PDF/A-1B"

                response = client.post(url="/pdf/meta", files={"file": pdf_file})
                assert response.status_code == 200
                assert response.json()["pdfVersion"] == "1.4"
                assert response.json()["pdfaClaim"] == "1B"


def test_libreoffice_convert_pdfa2():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/doc/word_document.docx"), "rb") as f:
        response = client.post(
            url="/libreoffice/convert?profile=pdfa-2b", files={"file": f}
        )
        assert response.status_code == 200
        with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
            tmp.write(response.content)
            with open(tmp.name, "rb") as pdf_file:
                response = client.post(url="/pdfa/validate", files={"file": pdf_file})
                assert response.status_code == 200
                assert response.json()["compliant"] is True
                assert response.json()["profile"] == "PDF/A-2B"

                response = client.post(url="/pdf/meta", files={"file": pdf_file})
                assert response.status_code == 200
                assert response.json()["pdfVersion"] == "1.7"
                assert response.json()["pdfaClaim"] == "2B"


def test_libreoffice_convert_pdfa3():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/doc/word_document.docx"), "rb") as f:
        response = client.post(
            url="/libreoffice/convert?profile=pdfa-3b", files={"file": f}
        )
        assert response.status_code == 200
        with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
            tmp.write(response.content)
            with open(tmp.name, "rb") as pdf_file:
                response = client.post(url="/pdfa/validate", files={"file": pdf_file})
                assert response.status_code == 200
                assert response.json()["compliant"] is True
                assert response.json()["profile"] == "PDF/A-3B"

                response = client.post(url="/pdf/meta", files={"file": pdf_file})
                assert response.status_code == 200
                assert response.json()["pdfVersion"] == "1.7"
                assert response.json()["pdfaClaim"] == "3B"


def test_libreoffice_convert_wrong_file_type():
    client = TestClient(api.app, raise_server_exceptions=False)
    with tempfile.NamedTemporaryFile(suffix=".xyz") as tmp:
        tmp.write(b"fff")
        response = client.post(url="/libreoffice/convert", files={"file": tmp})
        assert response.status_code == 400
        assert response.json() == {
            "message": "file extension '.xyz' is not supported ("
            + os.path.basename(tmp.name)
            + ")."
        }
