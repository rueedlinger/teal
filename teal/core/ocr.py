import io
import logging
import os
import tempfile

import aiofiles
from PyPDF2 import PdfReader, PdfWriter
from starlette.background import BackgroundTask
from starlette.responses import JSONResponse, FileResponse

from teal.core import (
    cleanup_tmp_dir,
    make_tesseract_lang_param,
    parse_page_ranges,
    get_tesseract_languages,
    get_file_ext,
)
from teal.core.cmd import AsyncSubprocess
from teal.core.http import create_json_err_response
from teal.model.ocr import OutputType, OcrMode

_logger = logging.getLogger("teal.ocr")


class PdfOcrAdapter:
    def __init__(self, ocrmypdf_cmd="ocrmypdf"):
        self.ocrmypdf_cmd = ocrmypdf_cmd
        self.supported_file_extensions = [".pdf"]
        self.supported_languages = get_tesseract_languages()

    async def create_pdf(
        self,
        data: bytes,
        filename: str,
        langs: list[str],
        output_type: OutputType,
        ocr_mode: OcrMode,
        page_ranges: str,
    ) -> FileResponse | JSONResponse:
        file_ext = get_file_ext(filename)
        if file_ext not in self.supported_file_extensions:
            return create_json_err_response(
                400,
                f"file extension '{file_ext}' is not supported, supported "
                f"extensions are {sorted(self.supported_file_extensions)}.",
            )

        # create tmp dir for all files
        tmp_dir = tempfile.mktemp(prefix="teal-")
        _logger.debug(f"creating tmp dir: {tmp_dir}")
        os.mkdir(tmp_dir)

        tmp_file_in_path = os.path.join(tmp_dir, "in-tmp.pdf")
        tmp_file_out_path = os.path.join(tmp_dir, "out-tmp.pdf")

        pages = parse_page_ranges(page_ranges)
        if pages is None:
            async with aiofiles.open(tmp_file_in_path, "wb") as tmp_file_in:
                _logger.debug(f"writing file {filename} to {tmp_file_in_path}")
                await tmp_file_in.write(data)
        else:
            _logger.debug(
                f"writing pages {pages} from {filename} to {tmp_file_in_path}"
            )
            await self._reduce_pages(data, pages, tmp_file_in_path)

        languages = make_tesseract_lang_param(langs)
        if languages is None:
            languages = "eng"

        if output_type is None:
            output_type = OutputType.PDF

        if ocr_mode is None:
            ocr_mode = OcrMode.SKIP_TEXT

        cmd_convert_pdf = f'{self.ocrmypdf_cmd} -l {languages} {ocr_mode.to_param()} --output-type {output_type.to_param()} "{tmp_file_in_path}" "{tmp_file_out_path}"'

        _logger.debug(f"running cmd: {cmd_convert_pdf}")
        proc = AsyncSubprocess(cmd_convert_pdf, tmp_dir)
        result = await proc.run()

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

    @staticmethod
    async def _reduce_pages(data, pages, tmp_file_in_path):
        infile = PdfReader(io.BytesIO(data), strict=False)
        output = PdfWriter()
        for i in pages:
            p = infile.pages[i - 1]
            output.add_page(p)
        with open(tmp_file_in_path, "wb") as tmp_file_in:
            output.write(tmp_file_in)
