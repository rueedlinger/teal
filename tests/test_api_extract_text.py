import tempfile

import pytest
from starlette.testclient import TestClient

from teal import api
from teal.model.extract import TextExtractMode
from tests import get_path


@pytest.mark.parametrize(
    "file,mode",
    [
        ("data/ocr/scanned_document.pdf", TextExtractMode.OCR),
        ("data/digital_pdf/document_two_pages.pdf", TextExtractMode.RAW),
    ],
)
def test_extract_text_with_mode(file, mode):
    client = TestClient(api.create_app(), raise_server_exceptions=False)
    with open(get_path(file), "rb") as f:
        response = client.post(
            url=f"/extract/text?mode={mode.value}", files={"file": f}
        )
        assert response.status_code == 200
        for i, r in enumerate(response.json()):
            assert len(r["text"]) > 1000
            assert r["mode"] == mode.value
            assert r["page"] == i + 1


@pytest.mark.parametrize(
    "file,pages,expected",
    [
        ("data/digital_pdf/document_multiple_pages.pdf", "1", 1),
        ("data/digital_pdf/document_multiple_pages.pdf", "1-2", 2),
        ("data/digital_pdf/document_multiple_pages.pdf", "1-2,5", 3),
    ],
)
def test_extract_text_with_pages(file, pages, expected):
    client = TestClient(api.create_app(), raise_server_exceptions=False)
    with open(get_path(file), "rb") as f:
        response = client.post(url=f"/extract/text?pages={pages}", files={"file": f})

        assert response.status_code == 200
        assert len(response.json()) == expected
        for i, r in enumerate(response.json()):
            assert len(r["text"]) > 1000
            assert r["mode"] == TextExtractMode.RAW.value


@pytest.mark.parametrize(
    "file,lang1,lang2",
    [
        ("data/digital_pdf/document_two_pages.pdf", "eng", "fra"),
    ],
)
def test_extract_text_with_languages(file, lang1, lang2):
    client = TestClient(api.create_app(), raise_server_exceptions=False)
    with open(get_path(file), "rb") as f:
        response = client.post(
            url=f"/extract/text?languages={lang1}&languages={lang2}&mode=ocr",
            files={"file": f},
        )

        assert response.status_code == 200
        for i, r in enumerate(response.json()):
            assert len(r["text"]) > 1000
            assert r["mode"] == TextExtractMode.OCR.value
            assert r["page"] == i + 1


def test_extract_text_with_wrong_file_ending():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/doc/word_document.docx"), "rb") as f:
        response = client.post(url="/extract/text", files={"file": f})
        assert response.status_code == 400
        assert response.json() == {
            "message": f"file extension '.docx' is not supported (word_document.docx)."
        }


def test_extract_text_with_unsupported_param():
    client = TestClient(api.create_app(), raise_server_exceptions=False)
    with open(get_path("data/digital_pdf/document_two_pages.pdf"), "rb") as f:
        response = client.post(url=f"/extract/text?foo=ddd", files={"file": f})
        assert response.status_code == 400
        unknown_params = ["foo"]
        known_params = sorted(["pages", "mode", "languages"])
        assert response.json() == {
            "message": f"Unknown request parameters: {unknown_params}, supported parameters are {known_params}"
        }


def test_pdf_extract_meta_corrupt_file():
    client = TestClient(api.app, raise_server_exceptions=False)
    with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
        tmp.write(b"fff")
        response = client.post(url="/extract/text", files={"file": tmp})
        assert response.status_code == 500
