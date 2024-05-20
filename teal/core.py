import logging
import os
import shutil

from starlette.background import BackgroundTask
from starlette.responses import JSONResponse

# get root logger
_logger = logging.getLogger("teal.core")


def create_json_response(content, background: BackgroundTask = None):
    return JSONResponse(content=content, background=background)


def create_json_err_response_from_exception(ex: Exception, background: BackgroundTask = None):
    return JSONResponse(
        status_code=500,
        content={
            "message": f"{ex}",
        },
        background=background
    )


def create_json_err_response(code: int, message: str, background: BackgroundTask = None):
    return JSONResponse(
        status_code=code,
        content={
            "message": message,
        },
        background=background
    )


def is_feature_enabled(feature_flag) -> bool:
    if feature_flag not in os.environ:
        return True

    if feature_flag in os.environ:
        return os.environ[feature_flag].lower() == 'true'


def cleanup_tmp_dir(tmp_dir: str):
    teal_tmp_dir_prefix = '/tmp/teal-'
    if tmp_dir.startswith(teal_tmp_dir_prefix):
        if os.path.exists(tmp_dir):
            _logger.debug(f"cleanup tmp dir {tmp_dir}")
            shutil.rmtree(tmp_dir)
        else:
            _logger.warning(f"will not delete '{tmp_dir}', tmp does not exists.")
    else:
        _logger.warning(f"will not delete '{tmp_dir}', tmp dir must start with '{teal_tmp_dir_prefix}'")
