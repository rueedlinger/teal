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
