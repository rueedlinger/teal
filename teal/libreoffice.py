import logging
import os
import subprocess
import tempfile

from starlette.background import BackgroundTask
from starlette.responses import FileResponse

_logger = logging.getLogger("teal.libreoffice")


class LibreOfficeAdapter:
    def __init__(self, libreoffice_path='soffice'):
        self.libreoffice_path = libreoffice_path

    def convert_to_pdf(self, data, filename):
        # create tmp dir for all files
        tmp_dir = tempfile.mktemp()
        _logger.debug(f"creating tmp dir: {tmp_dir}")
        os.mkdir(tmp_dir)

        tmp_file_in_path = os.path.join(tmp_dir, f"tmp{os.path.splitext(filename)[1]}")
        tmp_file_out_path = os.path.join(tmp_dir, "tmp.pdf")
        _logger.debug(f"in_file: {tmp_file_in_path}, out_file: {tmp_file_out_path}")

        with open(tmp_file_in_path, 'wb') as tmp_file_in:
            _logger.debug(f"writing file {filename} to {tmp_file_in_path}")
            tmp_file_in.write(data)

        _logger.debug(f"expecting out pdf {tmp_file_in_path}")
        cmd_convert_pdf = f'{self.libreoffice_path} --headless --convert-to pdf --outdir "{tmp_dir}" "{tmp_file_in_path}"'

        _logger.debug(f"running cmd: {cmd_convert_pdf}")
        result = subprocess.run(cmd_convert_pdf, shell=True, capture_output=True)

        if os.path.exists(tmp_file_out_path):
            _logger.debug(f"out was written {tmp_file_out_path}")
            return FileResponse(tmp_file_out_path, media_type='application/pdf',
                                filename=f"{os.path.splitext(filename)[0]}.pdf",
                                background=BackgroundTask(_cleanup, tmp_dir))

        else:
            _logger.debug(f"file was not written {result}")
            raise Exception(
                f"conversion error ({filename}) {str(result.stderr, 'utf-8')}")


def _cleanup(tmp_dir):
    _logger.debug(f"cleanup tmp dir {tmp_dir}")
    # shutil.rmtree(tmp_dir)
