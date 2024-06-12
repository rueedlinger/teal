import logging
import os
import tempfile

import pikepdf
from starlette.background import BackgroundTask
from starlette.responses import FileResponse, JSONResponse

from teal.core import (
    cleanup_tmp_dir,
    parse_page_ranges,
    to_page_range,
)
from teal.core.cmd import AsyncSubprocess
from teal.core.http import create_json_err_response
from teal.model.create import OutputType

_logger = logging.getLogger("teal.libreoffice")


class LibreOfficeAdapter:
    def __init__(self, libreoffice_cmd="soffice"):
        self.libreoffice_cmd = libreoffice_cmd
        self.supported_file_extensions = [
            ".doc",
            ".docx",
            ".odt",
            ".rtf",
            ".txt",
            ".pdf",
        ]

    async def create_pdf(
        self,
        data: bytes,
        filename: str,
        output_type: OutputType,
        page_ranges: str,
    ) -> FileResponse | JSONResponse:

        file_ext = os.path.splitext(filename)[1]
        if file_ext not in self.supported_file_extensions:
            return create_json_err_response(
                400, f"file extension '{file_ext}' is not supported ({filename})."
            )

        # create tmp dir for all files
        tmp_dir = tempfile.mktemp(prefix="teal-")
        _logger.debug(f"creating tmp dir: {tmp_dir}")
        os.mkdir(tmp_dir)

        tmp_file_in_path = os.path.join(tmp_dir, f"tmp{file_ext}")
        tmp_out_dir = os.path.join(tmp_dir, "out")

        with open(tmp_file_in_path, "wb") as tmp_file_in:
            _logger.debug(f"writing file {filename} to {tmp_file_in_path}")
            tmp_file_in.write(data)

        _logger.debug(f"expecting out pdf {tmp_file_in_path}")

        if output_type is None:
            # use default pdf version from libreoffice
            pdf_version = "0"
        else:
            pdf_version = output_type.to_param()

        pages = parse_page_ranges(page_ranges)
        _logger.debug(f"using pdf version {pdf_version}")

        # https://help.libreoffice.org/latest/en-US/text/shared/guide/pdf_params.html?&DbPAR=SHARED&System=UNIX
        if pages is None:
            pdf_param = (
                'pdf:draw_pdf_Export:{"SelectPdfVersion":{"type":"long","value":"'
                + pdf_version
                + '"}}'
            )
        else:
            pdf_param = (
                'pdf:draw_pdf_Export:{"SelectPdfVersion":{"type":"long","value":"'
                + pdf_version
                + '"},"PageRange":{"type":"string","value":"'
                + to_page_range(pages)
                + '"}}'
            )

        cmd_convert_pdf = f'{self.libreoffice_cmd} --headless --convert-to \'{pdf_param}\' --outdir "{tmp_out_dir}" "{tmp_file_in_path}"'

        _logger.debug(f"running cmd: {cmd_convert_pdf}")

        proc = AsyncSubprocess(cmd_convert_pdf, tmp_dir)
        """
        result = subprocess.run(
            cmd_convert_pdf,
            shell=True,
            capture_output=True,
            text=True,
            env={"HOME": tmp_dir},
        )
        """
        result = await proc.run()

        converted_file_out = os.path.join(tmp_dir, "out", "tmp.pdf")

        if result.returncode == 0:
            if os.path.exists(converted_file_out):
                # workaround: fix metadata PDF/A-1b error in libreoffice
                # edit metadata (this will fix xmp/docinfo metadata creation time difference bug)
                fixed_file = os.path.join(tmp_dir, "out", "fixed.pdf")
                pdf = pikepdf.open(converted_file_out)
                with pdf.open_metadata() as meta:
                    meta["xmp:CreatorTool"] = "LibreOffice"
                pdf.save(fixed_file)
                pdf.close()

                return FileResponse(
                    fixed_file,
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
