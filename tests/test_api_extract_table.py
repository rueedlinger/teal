import tempfile

import pytest
from starlette.testclient import TestClient

from teal import api
from tests import get_path


def test_pdf_table_extract_from_single_table():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/digital_pdf/document_with_one_table.pdf"), "rb") as f:
        response = client.post(url="/extract/table", files={"file": f})
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["page"] == 1
        assert response.json()[0]["index"] == 0
        assert response.json()[0]["table"] == [
            {"0": "A", "1": "B", "2": "C"},
            {"0": "A1", "1": "B11", "2": "C111"},
            {"0": "A2", "1": "B22", "2": "C222"},
            {"0": "A3", "1": "B33", "2": "C333"},
        ]


def test_pdf_table_extract_from_multiple_tables():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(
        get_path("data/digital_pdf/document_with_multiple_tables.pdf"), "rb"
    ) as f:
        response = client.post(url="/extract/table", files={"file": f})
        assert response.status_code == 200
        assert len(response.json()) == 3
        assert response.json()[0]["page"] == 1
        assert response.json()[0]["index"] == 0
        assert response.json()[0]["table"] == [
            {"0": "A", "1": "B", "2": "C", "3": "D"},
            {"0": "A1", "1": "B1", "2": "C1", "3": "D1"},
            {"0": "A2", "1": "B2", "2": "C2", "3": "D2"},
            {"0": "A3", "1": "B3", "2": "C3", "3": "D3"},
            {"0": "A4", "1": "B4", "2": "C4", "3": "D4"},
        ]

        assert response.json()[1]["page"] == 1
        assert response.json()[1]["index"] == 1
        assert response.json()[1]["table"] == [
            {"0": "AA", "1": "BB", "2": "CC", "3": "DD"},
            {"0": "AA1", "1": "BB1", "2": "CC1", "3": "DD1"},
            {"0": "AA2", "1": "BB2", "2": "CC2", "3": "DD2"},
            {"0": "AA3", "1": "BB3", "2": "CC3", "3": "DD3"},
            {"0": "AA4", "1": "BB4", "2": "CC4", "3": "DD4"},
        ]

        assert response.json()[2]["page"] == 2
        assert response.json()[2]["index"] == 0
        assert response.json()[2]["table"] == [
            {"0": "X", "1": "Y"},
            {"0": "X1", "1": "Y1"},
            {"0": "X2", "1": "Y2"},
            {"0": "X3", "1": "Y3"},
            {"0": "X4", "1": "Y4"},
        ]


@pytest.mark.parametrize(
    "file,pages,expected_pages,expected_tables",
    [
        ("data/digital_pdf/document_with_multiple_tables.pdf", "1", 1, 2),
        ("data/digital_pdf/document_with_multiple_tables.pdf", "1,2", 2, 3),
        ("data/digital_pdf/document_with_multiple_tables.pdf", "1-2", 2, 3),
        ("data/digital_pdf/document_with_multiple_tables.pdf", "2-2", 1, 1),
    ],
)
def test_pdf_table_extract_with_pages(file, pages, expected_pages, expected_tables):
    client = TestClient(api.create_app(), raise_server_exceptions=False)
    with open(get_path(file), "rb") as f:
        response = client.post(url=f"/extract/table?pages={pages}", files={"file": f})

        assert response.status_code == 200
        assert len(response.json()) == expected_tables

        count_pages = set()

        for i, r in enumerate(response.json()):
            assert len(r["table"]) > 3
            count_pages.add(r["page"])

        assert len(count_pages) == expected_pages


def test_pdf_table_extract_with_wrong_file_ending():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/doc/word_document.docx"), "rb") as f:
        response = client.post(url="/extract/table", files={"file": f})
        assert response.status_code == 400
        assert response.json() == {
            "message": f"file extension '.docx' is not supported (word_document.docx)."
        }


def test_pdf_table_extract_with_unsupported_param():
    client = TestClient(api.create_app(), raise_server_exceptions=False)
    with open(
        get_path("data/digital_pdf/document_with_multiple_tables.pdf"), "rb"
    ) as f:
        response = client.post(url=f"/extract/table?foo=ddd", files={"file": f})
        assert response.status_code == 400
        unknown_params = ["foo"]
        known_params = ["pages"]
        assert response.json() == {
            "message": f"Unknown request parameters: {unknown_params}, supported parameters are {known_params}"
        }


def test_pdf_table_meta_corrupt_file():
    client = TestClient(api.app, raise_server_exceptions=False)
    with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
        tmp.write(b"fff")
        response = client.post(url="/extract/table", files={"file": tmp})
        assert response.status_code == 500
