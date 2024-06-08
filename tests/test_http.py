import json

from teal.http import create_json_err_response_from_exception, create_json_err_response


def test_exception_mapping():
    resp = create_json_err_response_from_exception(Exception("ops!"))
    assert resp.status_code == 500
    assert json.loads(resp.body) == {"message": "ops!"}


def test_create_json_err_msg():
    resp = create_json_err_response(code=431, message="foo bar")
    assert resp.status_code == 431
    assert json.loads(resp.body) == {"message": "foo bar"}
