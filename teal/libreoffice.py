import logging
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from starlette.background import BackgroundTask
from starlette.responses import FileResponse

_logger = logging.getLogger("teal.libreoffice")


class LibreOfficeAdapter:
    def __init__(self, libreoffice_path='libreoffice'):
        self.libreoffice_path = libreoffice_path

    def convert_to_pdf(self, data, filename):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file_in_path = os.path.join(tmp_dir, filename)
            tmp_out_path = tempfile.mktemp()
            os.mkdir(tmp_out_path)
            new_file_name = Path(filename).stem + ".pdf"
            out_file = os.path.join(tmp_out_path, new_file_name)

            with open(tmp_file_in_path, 'wb') as tmp_file:
                _logger.debug(f"writing tmp file for input {tmp_file_in_path}")
                tmp_file.write(data)

                result = subprocess.run(
                    f'{self.libreoffice_path} \
                        --headless \
                        --convert-to pdf \
                        --outdir {tmp_out_path} {tmp_file_in_path}',
                    shell=True,
                    capture_output=True,
                    env={"HOME": "/tmp"})

                if os.path.exists(out_file):
                    _logger.debug(f"out was written {out_file}")
                    return FileResponse(out_file, media_type='application/pdf', filename=new_file_name,
                                        background=BackgroundTask(_cleanup, tmp_out_path))

                else:
                    _logger.debug(f"file was not written {result}")
                    raise RuntimeError(f"could convert file: {result}")


def _cleanup(tmp_dir):
    _logger.debug(f"cleanup {tmp_dir}")
    shutil.rmtree(tmp_dir)
