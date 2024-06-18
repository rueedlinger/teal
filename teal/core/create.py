import io
import logging
import os
import tempfile

import aiofiles
import pikepdf
from PyPDF2 import PdfReader, PdfWriter
from starlette.background import BackgroundTask
from starlette.responses import FileResponse, JSONResponse

from teal.core import (
    cleanup_tmp_dir,
    parse_page_ranges,
    to_page_range,
    get_file_ext,
    is_feature_enabled,
)
from teal.core.cmd import AsyncSubprocess
from teal.core.http import create_json_err_response
from teal.model.create import PdfOutputType, DocOutputType

_logger = logging.getLogger("teal.create")


class LibreOfficeAdapter:
    def __init__(self, libreoffice_cmd="soffice"):
        self.libreoffice_cmd = libreoffice_cmd
        self.create_doc_supported_file_extensions = [".pdf"]
        # at the moment restricted to these file endings
        self.create_pdf_supported_file_extensions = [
            # OpenDocument Text
            ".odt",
            # OpenDocument Text Template
            ".ott",
            # Rich Text Format
            ".rtf",
            # Microsoft Word
            ".doc",
            # Microsoft Word XML
            ".docx",
            # Plain Text
            ".txt",
            # Plain Text
            ".text",
            # PDF
            ".pdf",
        ]

    async def create_pdf(
        self,
        data: bytes,
        filename: str,
        output_type: PdfOutputType,
        page_ranges: str,
    ) -> FileResponse | JSONResponse:

        file_ext = get_file_ext(filename)
        if is_feature_enabled("TEAL_FEATURE_CREATE_PDF_CHECK_FILE_EXTENSION"):
            if file_ext not in self.create_pdf_supported_file_extensions:
                return create_json_err_response(
                    400,
                    f"file extension '{file_ext}' is not supported, supported "
                    f"extensions are {sorted(self.create_pdf_supported_file_extensions)}.",
                )

        # create tmp dir for all files
        tmp_dir = tempfile.mktemp(prefix="teal-")
        _logger.debug(f"creating tmp dir: {tmp_dir}")
        os.mkdir(tmp_dir)

        tmp_file_in_path = os.path.join(tmp_dir, f"tmp{file_ext}")
        tmp_out_dir = os.path.join(tmp_dir, "out")
        _logger.debug(f"tmp_file_in_path: {tmp_file_in_path}")
        _logger.debug(f"tmp_out_dir: {tmp_out_dir}")

        async with aiofiles.open(tmp_file_in_path, "wb") as tmp_file_in:
            _logger.debug(f"writing file {filename} to {tmp_file_in_path}")
            await tmp_file_in.write(data)

        if output_type is None:
            # use default pdf version from libreoffice
            pdf_version = "0"
        else:
            pdf_version = output_type.to_param()

        pages = parse_page_ranges(page_ranges)

        # https://help.libreoffice.org/latest/en-US/text/shared/guide/pdf_params.html?&DbPAR=SHARED&System=UNIX
        # https://help.libreoffice.org/latest/en-US/text/shared/guide/convertfilters.html?DbPAR=SHARED#bm_id541554406270299
        # https://vmiklos.hu/blog/pdf-convert-to.html
        if pages is None:
            pdf_param = (
                'pdf:writer_pdf_Export:{"SelectPdfVersion":{"type":"long","value":"'
                + pdf_version
                + '"}}'
            )
        else:
            pdf_param = (
                'pdf:writer_pdf_Export:{"SelectPdfVersion":{"type":"long","value":"'
                + pdf_version
                + '"},"PageRange":{"type":"string","value":"'
                + to_page_range(pages)
                + '"}}'
            )

        cmd_convert_pdf = f'{self.libreoffice_cmd} --headless --convert-to \'{pdf_param}\' --outdir "{tmp_out_dir}" "{tmp_file_in_path}"'
        _logger.debug(f"running cmd: {cmd_convert_pdf}")

        proc = AsyncSubprocess(cmd_convert_pdf, tmp_dir)
        result = await proc.run()

        converted_file_out = os.path.join(tmp_dir, "out", "tmp.pdf")

        if result.returncode == 0:
            if os.path.exists(converted_file_out):
                # workaround: fix metadata PDF/A-1b error in libreoffice
                # edit metadata (this will fix xmp/docinfo metadata creation time difference bug)
                fixed_file = os.path.join(tmp_dir, "out", "fixed.pdf")
                await self._modify_pdf_metadata(converted_file_out, fixed_file)
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

    async def create_doc(
        self,
        data: bytes,
        filename: str,
        output_type: DocOutputType,
        page_ranges: str,
    ) -> FileResponse | JSONResponse:
        file_ext = get_file_ext(filename)

        if file_ext not in self.create_doc_supported_file_extensions:
            return create_json_err_response(
                400,
                f"file extension '{file_ext}' is not supported, supported "
                f"extensions are {sorted(self.create_pdf_supported_file_extensions)}.",
            )

        # create tmp dir for all files
        tmp_dir = tempfile.mktemp(prefix="teal-")
        _logger.debug(f"creating tmp dir: {tmp_dir}")
        os.mkdir(tmp_dir)

        tmp_file_in_path = os.path.join(tmp_dir, f"tmp{file_ext}")
        tmp_out_dir = os.path.join(tmp_dir, "out")
        _logger.debug(f"tmp_file_in_path: {tmp_file_in_path}")
        _logger.debug(f"tmp_out_dir: {tmp_out_dir}")

        pages = parse_page_ranges(page_ranges)
        if pages is not None:
            _logger.debug(
                f"writing reduced file {filename} ({pages}) to {tmp_file_in_path}"
            )
            await self._reduce_pages(data, pages, tmp_file_in_path)
        else:
            async with aiofiles.open(tmp_file_in_path, "wb") as tmp_file_in:
                _logger.debug(f"writing file {filename} to {tmp_file_in_path}")
                await tmp_file_in.write(data)

        if output_type == DocOutputType.ODT:
            doc_param = "odt:writer8"
        elif output_type == DocOutputType.DOC:
            doc_param = "doc:MS Word 97"
        elif output_type == DocOutputType.DOCX:
            doc_param = "docx:MS Word 2007 XML"
        else:
            doc_param = "odt:writer8"

        # https://help.libreoffice.org/latest/en-US/text/shared/guide/convertfilters.html?DbPAR=SHARED#bm_id541554406270299
        cmd_convert_doc = f'{self.libreoffice_cmd} --infilter="writer_pdf_import" --headless --convert-to  "{doc_param}" --outdir "{tmp_out_dir}" "{tmp_file_in_path}"'
        _logger.debug(f"running cmd: {cmd_convert_doc}")

        proc = AsyncSubprocess(cmd_convert_doc, tmp_dir)
        result = await proc.run()

        if output_type is None:
            file_ext = ".odt"
        else:
            file_ext = output_type.to_file_ext()

        converted_file_out = os.path.join(tmp_dir, "out", f"tmp{file_ext}")
        _logger.info(converted_file_out)

        if result.returncode == 0:
            return FileResponse(
                converted_file_out,
                media_type="application/octet-stream",
                filename=f"{os.path.splitext(filename)[0]}{file_ext}",
                # background=BackgroundTask(cleanup_tmp_dir, tmp_dir),
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

    @staticmethod
    async def _modify_pdf_metadata(converted_file_out, fixed_file):
        with pikepdf.open(converted_file_out) as pdf:
            with pdf.open_metadata() as meta:
                meta["xmp:CreatorTool"] = "LibreOffice"
            pdf.save(fixed_file)
