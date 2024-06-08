import logging
import os
import re
import shutil

import PyPDF2
import camelot
import cv2
import fastapi
import pikepdf
import pypdfium2
import pytesseract

from teal.model import AppInfo

_logger = logging.getLogger("teal.core")


def is_feature_enabled(feature_flag) -> bool:
    if feature_flag not in os.environ:
        return True

    if feature_flag in os.environ:
        return os.environ[feature_flag].lower() == "true"


def get_version() -> str:
    if "TEAL_VERSION" in os.environ and len(os.environ["TEAL_VERSION"]) > 1:
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
    if "TEAL_TESSERACT_TESSDATA_PATH" in os.environ:
        path = os.environ["TEAL_TESSERACT_TESSDATA_PATH"]

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


def get_app_info() -> AppInfo:

    details = {}
    for k in os.environ.keys():
        if k.startswith("TEAL_"):
            details[k.lower().replace("teal_", "")] = os.environ[k]

    details["tesseract_languages"] = get_tesseract_languages()

    try:
        details["pike_version"] = pikepdf.__version__
    except Exception as e:
        details["pike_version"] = str(e)

    try:
        details["pytesseract_version"] = pytesseract.__version__
    except Exception as e:
        details["pytesseract_version"] = str(e)

    try:
        details["pypdf2_version"] = PyPDF2.__version__
    except Exception as e:
        details["pypdf2_version"] = str(e)

    try:
        details["pypdfium2_version"] = pypdfium2.V_PYPDFIUM2
    except Exception as e:
        details["pypdfium2_version"] = str(e)

    try:
        details["camelot_version"] = camelot.__version__
    except Exception as e:
        details["camelot_version"] = str(e)

    try:
        details["fastapi_version"] = fastapi.__version__
    except Exception as e:
        details["fastapi_version"] = str(e)

    try:
        details["opencv_version"] = cv2.__version__
    except Exception as e:
        details["opencv_version"] = str(e)

    return AppInfo.model_validate({"version": get_version(), "details": details})


def make_tesseract_lang_param(langs: list[str] | None) -> str | None:
    if langs is None:
        return None
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
