import os

import teal.core as core


def test_feature_flag():
    assert core.is_feature_enabled("foo_flag") is True

    os.environ["foo_flag"] = "true"
    assert core.is_feature_enabled("foo_flag") is True

    os.environ["foo_flag"] = "True"
    assert core.is_feature_enabled("foo_flag") is True

    os.environ["foo_flag"] = "false"
    assert core.is_feature_enabled("foo_flag") is False

    os.environ["foo_flag"] = "False"
    assert core.is_feature_enabled("foo_flag") is False


def test_tesseract_languages():
    assert len(core.get_tesseract_languages()) > 0


def test_make_tesseract_lang_param():
    assert core.make_tesseract_lang_param(None) is None

    assert core.make_tesseract_lang_param([]) is None

    assert core.make_tesseract_lang_param([""]) is None

    assert core.make_tesseract_lang_param(["eng"]) == "eng"

    assert core.make_tesseract_lang_param(["eng", "deu"]) == "eng+deu"

    assert core.make_tesseract_lang_param(["eng", "deu", "fra"]) == "eng+deu+fra"


def test_parse_page_ranges():
    assert core.parse_page_ranges(None) is None
    assert core.parse_page_ranges("") is None
    assert core.parse_page_ranges(" ") is None
    assert core.parse_page_ranges("1,2") == [1, 2]
    assert core.parse_page_ranges("1, 2 ") == [1, 2]
    assert core.parse_page_ranges("1,10") == [1, 10]
    assert core.parse_page_ranges("1-5") == [1, 2, 3, 4, 5]
    assert core.parse_page_ranges("1,2,4-7") == [1, 2, 4, 5, 6, 7]
    assert core.parse_page_ranges("1-2,4-7") == [1, 2, 4, 5, 6, 7]
    assert core.parse_page_ranges("1,4-7,1-5") == [1, 2, 3, 4, 5, 6, 7]
    assert core.parse_page_ranges("8,1") == [1, 8]
    assert core.parse_page_ranges("9-1") is None
    assert core.parse_page_ranges("9-1,1-2") == [1, 2]
    assert core.parse_page_ranges("e-1,1-2,z") == [1, 2]


def test_to_page_range():
    assert core.to_page_range([]) == ""
    assert core.to_page_range([1]) == "1"
    assert core.to_page_range([1, 2]) == "1,2"
    assert core.to_page_range([1, 2, 9]) == "1,2,9"
