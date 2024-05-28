import json
import logging
import os
import subprocess
import tempfile

from fastapi.encoders import jsonable_encoder
from starlette.background import BackgroundTask
from starlette.responses import JSONResponse, FileResponse

from teal.core import create_json_err_response, create_json_response, cleanup_tmp_dir
from teal.model import PdfAReport

_logger = logging.getLogger("teal.pdfa")


class PdfAConverter:
    def __init__(self, ocrmypdf_cmd="ocrmypdf"):
        self.ocrmypdf_cmd = ocrmypdf_cmd
        self.supported_file_extensions = [".pdf"]

    def convert_pdfa(self, data, filename) -> FileResponse | JSONResponse:
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in self.supported_file_extensions:
            return create_json_err_response(
                400, f"file extension '{file_ext}' is not supported ({filename})."
            )

        # create tmp dir for all files
        tmp_dir = tempfile.mktemp(prefix="teal-")
        _logger.debug(f"creating tmp dir: {tmp_dir}")
        os.mkdir(tmp_dir)

        tmp_file_in_path = os.path.join(tmp_dir, "in-tmp.pdf")
        tmp_file_out_path = os.path.join(tmp_dir, "out-tmp.pdf")

        with open(tmp_file_in_path, "wb") as tmp_file_in:
            _logger.debug(f"writing file {filename} to {tmp_file_in_path}")
            tmp_file_in.write(data)

        # see https://ocrmypdf.readthedocs.io/en/latest/advanced.html
        # -l eng+fra
        # --output-type {pdfa,pdf,pdfa-1,pdfa-2,pdfa-3,non
        # --skip-text then no image processing or OCR will be performed on pages that already
        # have text. The page will be copied to the output. This may be useful for documents that contain
        # both “born digital” and scanned content, or to use OCRmyPDF to normalize and convert to PDF/A
        # regardless of their contents.

        cmd_convert_pdf = f'{self.ocrmypdf_cmd} --skip-text --output-type pdfa "{tmp_file_in_path}" "{tmp_file_out_path}"'

        _logger.debug(f"running cmd: {cmd_convert_pdf}")
        result = subprocess.run(
            cmd_convert_pdf,
            shell=True,
            capture_output=True,
            text=True,
            env={"HOME": "/tmp"},
        )

        if result.returncode == 0:
            if os.path.exists(tmp_file_out_path):
                return FileResponse(
                    tmp_file_out_path,
                    media_type="application/pdf",
                    filename=f"{os.path.splitext(filename)[0]}.pdf",
                    background=BackgroundTask(cleanup_tmp_dir, tmp_dir),
                )
            else:
                _logger.debug(f"file was not written {result}")
                return create_json_err_response(
                    500,
                    f"could not convert file '{filename}' {result.stderr}",
                    background=BackgroundTask(cleanup_tmp_dir, tmp_dir),
                )
        else:
            _logger.debug(f"cmd was not successful {result}")
            return create_json_err_response(
                500,
                f"got return code {result.returncode} '{filename}' {result.stderr}",
                background=BackgroundTask(cleanup_tmp_dir, tmp_dir),
            )


class PdfAValidator:
    def __init__(self, verapdf_cmd="/usr/local/verapdf/verapdf"):
        self.verapdf_cmd = verapdf_cmd
        self.supported_file_extensions = [".pdf"]

    def validate_pdf(self, data, filename, profile="0") -> JSONResponse:
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in self.supported_file_extensions:
            return create_json_err_response(
                400, f"file extension '{file_ext}' is not supported ({filename})."
            )

        # create tmp dir for all files
        tmp_dir = tempfile.mktemp(prefix="teal-")
        _logger.debug(f"creating tmp dir: {tmp_dir}")
        os.mkdir(tmp_dir)

        tmp_file_in_path = os.path.join(tmp_dir, "in-tmp.pdf")
        tmp_file_out_path = os.path.join(tmp_dir, "out-tmp.json")

        with open(tmp_file_in_path, "wb") as tmp_file_in:
            _logger.debug(f"writing file {filename} to {tmp_file_in_path}")
            tmp_file_in.write(data)

        if profile is None:
            profile = "0"

        cmd_convert_pdf = f'{self.verapdf_cmd} -f {profile} --format json "{tmp_file_in_path}" > "{tmp_file_out_path}"'

        _logger.debug(f"running cmd: {cmd_convert_pdf}")
        result = subprocess.run(
            cmd_convert_pdf,
            shell=True,
            capture_output=True,
            text=True,
            env={"HOME": "/tmp"},
        )
        _logger.debug(f"got result {result}")

        if result.returncode == 0 or result.returncode == 1:

            with open(tmp_file_out_path) as tmp_json:
                report = json.load(tmp_json)
                out = report["report"]["jobs"][0]["validationResult"]
                out["profile"] = report["report"]["jobs"][0]["validationResult"][
                    "profileName"
                ].split(" ")[0]
                return create_json_response(
                    content=jsonable_encoder(PdfAReport.model_validate(out)),
                    background=BackgroundTask(cleanup_tmp_dir, tmp_dir),
                )
                # return report['report']['jobs'][0]['validationResult']
        else:
            _logger.debug(f"cmd was not successful {result}")
            return create_json_err_response(
                500,
                f"got return code {result.returncode} '{filename}' {result.stderr}",
                background=BackgroundTask(cleanup_tmp_dir, tmp_dir),
            )
