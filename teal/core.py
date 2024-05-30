import logging
import os
import re
import shutil

from starlette.background import BackgroundTask
from starlette.responses import JSONResponse

# get root logger
_logger = logging.getLogger("teal.core")


def create_json_response(content, background: BackgroundTask = None):
    return JSONResponse(content=content, background=background)


def create_json_err_response_from_exception(
    ex: Exception, background: BackgroundTask = None
):
    return JSONResponse(
        status_code=500,
        content={
            "message": f"{ex}",
        },
        background=background,
    )


def create_json_err_response(
    code: int, message: str, background: BackgroundTask = None
):
    return JSONResponse(
        status_code=code,
        content={
            "message": message,
        },
        background=background,
    )


def is_feature_enabled(feature_flag) -> bool:
    if feature_flag not in os.environ:
        return True

    if feature_flag in os.environ:
        return os.environ[feature_flag].lower() == "true"


def get_version() -> str:
    if "TEAL_VERSION" in os.environ:
        return os.environ["TEAL_VERSION"]
    return "unknown"


def cleanup_tmp_dir(tmp_dir: str):
    teal_tmp_dir_prefix = "/tmp/teal-"
    if tmp_dir.startswith(teal_tmp_dir_prefix):
        if os.path.exists(tmp_dir):
            _logger.debug(f"cleanup tmp dir {tmp_dir}")
            shutil.rmtree(tmp_dir)
        else:
            _logger.warning(f"will not delete '{tmp_dir}', tmp does not exists.")
    else:
        _logger.warning(
            f"will not delete '{tmp_dir}', tmp dir must start with '{teal_tmp_dir_prefix}'"
        )


def get_tesseract_languages() -> list[str]:
    path = "/usr/share/tesseract-ocr/5/tessdata"
    if "TESSERACT_TESSDATA_PATH" in os.environ:
        path = os.environ["TESSERACT_TESSDATA_PATH"]

    if os.path.exists(path):
        languages = [
            f.replace(".traineddata", "")
            for f in os.listdir(path)
            if re.match(r"[a-zA-Z_]+.*\.traineddata", f)
        ]
        return languages
    else:
        _logger.warning(f"not tesseract languages found in path {path}")
        return []


def make_tesseract_lang_param(langs: list[str]) -> str | None:
    if len(langs) == 0:
        return None
    if len(langs) == 1 and langs[0] == "":
        return None
    return "+".join(langs)


def parse_page_ranges(range_string):
    if range_string is None:
        return None

    result = []
    elements = range_string.split(",")

    for element in elements:
        if "-" in element:
            try:
                start, end = map(int, element.split("-"))
                result.extend(range(start, end + 1))
            except ValueError as e:
                _logger.warning(f"ignoring invalid range input {element}")
        else:
            try:
                result.append(int(element))
            except ValueError as e:
                _logger.warning(f"ignoring invalid input {element}")

    if len(result) == 0:
        return None

    return sorted(set(result))


def to_page_range(ranges: list[int]) -> str:
    return ",".join([str(e) for e in ranges])
