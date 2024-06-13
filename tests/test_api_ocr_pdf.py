import tempfile

import pytest
from starlette.testclient import TestClient

from teal import api
from teal.model.ocr import OcrMode, OutputType
from tests import get_path


@pytest.mark.parametrize(
    "file",
    ["data/ocr/scanned_document.pdf", "data/digital_pdf/document_two_pages.pdf"],
)
def test_ocr_pdf_with_default(file):
    client = TestClient(api.create_app(), raise_server_exceptions=False)
    with open(get_path(file), "rb") as f:
        response = client.post(url="/ocr/pdf", files={"file": f})
        assert response.status_code == 200

        with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
            tmp.write(response.content)
            with open(tmp.name, "rb") as pdf_file:
                response = client.post(
                    url="/extract/text?mode=raw", files={"file": pdf_file}
                )
                assert response.status_code == 200
                assert len(response.json()) > 1
                for r in response.json():
                    assert len(r["text"]) > 1000
                    assert r["mode"] == "raw"


@pytest.mark.parametrize(
    "file,ocr_mode",
    [
        ("data/ocr/scanned_document.pdf", OcrMode.REDO_OCR),
        ("data/digital_pdf/document_two_pages.pdf", OcrMode.REDO_OCR),
        ("data/ocr/scanned_document.pdf", OcrMode.SKIP_TEXT),
        ("data/digital_pdf/document_two_pages.pdf", OcrMode.SKIP_TEXT),
        ("data/ocr/scanned_document.pdf", OcrMode.FORCE_OCR),
        ("data/digital_pdf/document_two_pages.pdf", OcrMode.FORCE_OCR),
    ],
)
def test_ocr_pdf_with_orc_mode(file, ocr_mode):
    client = TestClient(api.create_app(), raise_server_exceptions=False)
    with open(get_path(file), "rb") as f:
        response = client.post(url=f"/ocr/pdf?ocr={ocr_mode.value}", files={"file": f})
        assert response.status_code == 200

        with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
            tmp.write(response.content)
            with open(tmp.name, "rb") as pdf_file:
                response = client.post(
                    url="/extract/text?mode=raw", files={"file": pdf_file}
                )
                assert response.status_code == 200
                assert len(response.json()) > 1
                for r in response.json():
                    assert len(r["text"]) > 1000
                    assert r["mode"] == "raw"


@pytest.mark.parametrize(
    "file,pages,expected",
    [
        ("data/digital_pdf/document_multiple_pages.pdf", "1", 1),
        ("data/digital_pdf/document_multiple_pages.pdf", "1-2", 2),
        ("data/digital_pdf/document_multiple_pages.pdf", "1-2,5", 3),
    ],
)
def test_ocr_pdf_with_pages(file, pages, expected):
    client = TestClient(api.create_app(), raise_server_exceptions=False)
    with open(get_path(file), "rb") as f:
        response = client.post(url=f"/ocr/pdf?pages={pages}", files={"file": f})
        assert response.status_code == 200

        with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
            tmp.write(response.content)
            with open(tmp.name, "rb") as pdf_file:
                response = client.post(
                    url="/extract/text?mode=raw", files={"file": pdf_file}
                )
                assert response.status_code == 200
                assert len(response.json()) == expected

                for r in response.json():
                    assert len(r["text"]) > 1000
                    assert r["mode"] == "raw"


@pytest.mark.parametrize(
    "file,output,expected_version",
    [
        ("data/ocr/scanned_document.pdf", OutputType.PDF, "1.5"),
        ("data/digital_pdf/document_multiple_pages.pdf", OutputType.PDF, "1.5"),
        ("data/ocr/scanned_document.pdf", OutputType.PDFA_1B, "1.4"),
        ("data/digital_pdf/document_multiple_pages.pdf", OutputType.PDFA_1B, "1.4"),
        ("data/ocr/scanned_document.pdf", OutputType.PDFA_2B, "1.7"),
        ("data/digital_pdf/document_multiple_pages.pdf", OutputType.PDFA_2B, "1.7"),
        ("data/ocr/scanned_document.pdf", OutputType.PDFA_3B, "1.6"),
        ("data/digital_pdf/document_multiple_pages.pdf", OutputType.PDFA_3B, "1.6"),
    ],
)
def test_ocr_pdf_with_output(file, output, expected_version):
    client = TestClient(api.create_app(), raise_server_exceptions=False)
    with open(get_path(file), "rb") as f:
        response = client.post(url=f"/ocr/pdf?output={output.value}", files={"file": f})
        assert response.status_code == 200

        with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
            tmp.write(response.content)
            with open(tmp.name, "rb") as pdf_file:

                response = client.post(url="/extract/meta", files={"file": pdf_file})
                assert response.status_code == 200
                assert response.json()["pdfVersion"] == expected_version

                response = client.post(
                    url=f"/validate/pdfa",
                    files={"file": pdf_file},
                )
                assert response.status_code == 200

                if output.value is not OutputType.PDF.value:
                    assert response.json()["compliant"] is True
                    assert response.json()["profile"] == output.value.upper().replace(
                        "A", "/A"
                    )
                else:
                    assert response.json()["compliant"] is False

                response = client.post(
                    url="/extract/text?mode=raw", files={"file": pdf_file}
                )

                assert response.status_code == 200
                assert len(response.json()) > 1
                for r in response.json():
                    assert len(r["text"]) > 200
                    assert r["mode"] == "raw"


@pytest.mark.parametrize(
    "file,lang1,lang2",
    [
        ("data/ocr/scanned_document.pdf", "eng", "fra"),
        ("data/digital_pdf/document_two_pages.pdf", "eng", "fra"),
    ],
)
def test_ocr_pdf_with_languages(file, lang1, lang2):
    client = TestClient(api.create_app(), raise_server_exceptions=False)
    with open(get_path(file), "rb") as f:
        response = client.post(
            url=f"/ocr/pdf?languages={lang1}&languages={lang2}", files={"file": f}
        )
        assert response.status_code == 200

        with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
            tmp.write(response.content)
            with open(tmp.name, "rb") as pdf_file:
                response = client.post(
                    url="/extract/text?mode=raw", files={"file": pdf_file}
                )
                assert response.status_code == 200
                assert len(response.json()) > 1
                for r in response.json():
                    assert len(r["text"]) > 1000
                    assert r["mode"] == "raw"


def test_ocr_pdf_with_wrong_file_ending():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/doc/word_document.docx"), "rb") as f:
        response = client.post(url="/ocr/pdf", files={"file": f})
        assert response.status_code == 400
        assert response.json() == {
            "message": f"file extension '.docx' is not supported, supported extensions are ['.pdf']."
        }


def test_ocr_pdf_with_unsupported_param():
    client = TestClient(api.create_app(), raise_server_exceptions=False)
    with open(
        get_path("data/digital_pdf/document_with_multiple_tables.pdf"), "rb"
    ) as f:
        response = client.post(url=f"/ocr/pdf?foo=ddd", files={"file": f})
        assert response.status_code == 400
        unknown_params = ["foo"]
        known_params = sorted(["pages", "ocr", "output", "languages"])
        assert response.json() == {
            "message": f"Unknown request parameters: {unknown_params}, supported parameters are {known_params}"
        }


def test_ocr_pdf_corrupt_file():
    client = TestClient(api.app, raise_server_exceptions=False)
    with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
        tmp.write(b"fff")
        tmp.write(b"000")
        tmp.write(b"aaa")
        response = client.post(url="/ocr/pdf", files={"file": tmp})
        assert response.status_code == 500
