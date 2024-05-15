import os

from starlette.responses import JSONResponse


def create_json_err_response_from_exception(ex: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "message": f"{ex}",
        })


def create_json_err_response(code: int, message: str):
    return JSONResponse(
        status_code=code,
        content={
            "message": message,
        })


def is_feature_enabled(feature_flag) -> bool:
    if feature_flag not in os.environ:
        return True

    if feature_flag in os.environ:
        return os.environ[feature_flag].lower() == 'true'
