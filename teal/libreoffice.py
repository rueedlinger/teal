import logging
import os
import shutil
import subprocess
import tempfile

from starlette.background import BackgroundTask
from starlette.responses import FileResponse

_logger = logging.getLogger("teal.libreoffice")


class LibreOfficeAdapter:
    def __init__(self, libreoffice_path='soffice'):
        self.libreoffice_path = libreoffice_path

    def convert_to_pdf(self, data, filename):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file_in_path = os.path.join(tmp_dir, f"tmp{os.path.splitext(filename)[1]}")
            tmp_out_path = tempfile.mktemp()

            os.mkdir(tmp_out_path)
            out_file = os.path.join(tmp_out_path, "tmp.pdf")

            with open(tmp_file_in_path, 'wb') as tmp_file:
                _logger.debug(f"tmp input: '{tmp_file_in_path}', tmp output: '{out_file}'")
                tmp_file.write(data)

                result = subprocess.run(
                    f'{self.libreoffice_path} \
                        --headless \
                        --convert-to pdf \
                        --outdir "{tmp_out_path}" "{tmp_file_in_path}"',
                    shell=True,
                    capture_output=True,
                    env={"HOME": "/tmp"})

                if os.path.exists(out_file):
                    _logger.debug(f"out was written {out_file}")
                    return FileResponse(out_file, media_type='application/pdf',
                                        filename=f"{os.path.splitext(filename)[0]}.pdf",
                                        background=BackgroundTask(_cleanup, tmp_out_path))

                else:
                    _logger.debug(f"file was not written {result}")
                    raise Exception(
                        f"conversion error ({filename}) {str(result.stderr, 'utf-8')}")


def _cleanup(tmp_dir):
    _logger.debug(f"cleanup {tmp_dir}")
    shutil.rmtree(tmp_dir)
