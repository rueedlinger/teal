import json
import logging
import os
import subprocess
import tempfile

from teal.core import create_json_err_response

_logger = logging.getLogger("teal.pdfa")


class PdfAValidator:
    def __init__(self, verapdf_cmd='/usr/local/verapdf/verapdf'):
        self.verapdf_cmd = verapdf_cmd
        self.supported_file_extensions = ['.pdf']

    def validate_pdf(self, data, filename):
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in self.supported_file_extensions:
            return create_json_err_response(400, f"file extension '{file_ext}' is not supported ({filename}).")

        # create tmp dir for all files
        tmp_dir = tempfile.mktemp(prefix='teal-')
        _logger.debug(f"creating tmp dir: {tmp_dir}")
        os.mkdir(tmp_dir)

        tmp_file_in_path = os.path.join(tmp_dir, "in-tmp.pdf")
        tmp_file_out_path = os.path.join(tmp_dir, "out-tmp.json")

        with open(tmp_file_in_path, 'wb') as tmp_file_in:
            _logger.debug(f"writing file {filename} to {tmp_file_in_path}")
            tmp_file_in.write(data)

        cmd_convert_pdf = f'{self.verapdf_cmd} -f 0 --format json "{tmp_file_in_path}" > "{tmp_file_out_path}"'

        _logger.debug(f"running cmd: {cmd_convert_pdf}")
        result = subprocess.run(cmd_convert_pdf, shell=True, capture_output=True, text=True, env={'HOME': '/tmp'})
        _logger.debug(f"got result {result}")

        if result.returncode == 0 or result.returncode == 1:

            with open(tmp_file_out_path) as tmp_json:
                report = json.load(tmp_json)
                return report['report']['jobs'][0]['validationResult']
        else:
            _logger.debug(f"cmd was not successful {result}")
            return create_json_err_response(500, f"got return code {result.returncode} '{filename}' {result.stderr}")
