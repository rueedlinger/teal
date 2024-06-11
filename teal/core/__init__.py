import logging
import os
import re
import shutil
from typing import List

_logger = logging.getLogger("teal.core")


def default_logging_conf():
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "simple",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "teal": {"level": "INFO", "handlers": ["console"], "propagate": False},
            "uvicorn": {
                "level": "INFO",
                "handlers": ["console"],
                "propagate": False,
            },
        },
        "root": {"handlers": ["console"], "level": "WARN"},
    }


def is_feature_enabled(feature_flag: str) -> bool:
    if feature_flag not in os.environ:
        return True

    if feature_flag in os.environ:
        return os.environ[feature_flag].lower() == "true"


def get_version() -> str:
    if "TEAL_VERSION" in os.environ and len(os.environ["TEAL_VERSION"]) > 1:
        return os.environ["TEAL_VERSION"]
    return "unknown"


def get_file_ext(filename: str) -> str:
    return os.path.splitext(filename)[1].lower()


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


def make_tesseract_lang_param(langs: list[str] | None) -> str | None:
    if langs is None:
        return None
    if len(langs) == 0:
        return None
    if len(langs) == 1 and langs[0] == "":
        return None
    return "+".join(langs)


def parse_page_ranges(range_string: str) -> List[int] | None:
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
