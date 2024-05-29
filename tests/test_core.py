import json
import os

import teal.core as core


def test_exception_mapping():
    resp = core.create_json_err_response_from_exception(Exception("ops!"))
    assert resp.status_code == 500
    assert json.loads(resp.body) == {"message": "ops!"}


def test_create_json_err_msg():
    resp = core.create_json_err_response(code=431, message="foo bar")
    assert resp.status_code == 431
    assert json.loads(resp.body) == {"message": "foo bar"}


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
    assert core.make_tesseract_lang_param([]) is None

    assert core.make_tesseract_lang_param([""]) is None

    assert core.make_tesseract_lang_param(["eng"]) == "eng"

    assert core.make_tesseract_lang_param(["eng", "deu"]) == "eng+deu"

    assert core.make_tesseract_lang_param(["eng", "deu", "fra"]) == "eng+deu+fra"
