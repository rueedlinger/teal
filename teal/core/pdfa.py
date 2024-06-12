import json
import logging
import os
import tempfile

from fastapi.encoders import jsonable_encoder
from starlette.background import BackgroundTask
from starlette.responses import JSONResponse

from teal.core import (
    cleanup_tmp_dir,
)
from teal.core.cmd import AsyncSubprocess
from teal.core.http import create_json_err_response, create_json_response
from teal.model.validate import PdfAReport, ValidatePdfProfile

_logger = logging.getLogger("teal.pdfa")


class PdfAValidator:
    def __init__(self, verapdf_cmd="/usr/local/verapdf/verapdf"):
        self.verapdf_cmd = verapdf_cmd
        self.supported_file_extensions = [".pdf"]

    async def validate_pdf(
        self, data: bytes, filename: str, profile: ValidatePdfProfile
    ) -> JSONResponse:
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
            # Letting veraPDF control the profile choice
            profile_value = "0"
        else:
            profile_value = profile.value

        cmd_convert_pdf = f'{self.verapdf_cmd} -f {profile_value} --format json "{tmp_file_in_path}" > "{tmp_file_out_path}"'

        _logger.debug(f"running cmd: {cmd_convert_pdf}")
        proc = AsyncSubprocess(cmd_convert_pdf, tmp_dir)
        result = await proc.run()
        """
        result = subprocess.run(
            cmd_convert_pdf,
            shell=True,
            capture_output=True,
            text=True,
            env={"HOME": "/tmp"},
        )
        """
        _logger.debug(f"got result {result}")

        if result.returncode == 0 or result.returncode == 1:

            with open(tmp_file_out_path) as tmp_json:
                out = {
                    "profile": "NONE",
                    "statement": f"non of the profiles matched {[e.value for e in ValidatePdfProfile]}",
                    "compliant": False,
                }

                if profile is None and result.returncode == 1:
                    pass
                else:
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
