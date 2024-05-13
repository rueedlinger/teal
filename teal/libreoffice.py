import logging
import os
import subprocess
import tempfile

from starlette.background import BackgroundTask
from starlette.responses import FileResponse

from teal.core import create_json_err_response

_logger = logging.getLogger("teal.libreoffice")


class LibreOfficeAdapter:
    def __init__(self, libreoffice_cmd='soffice'):
        self.libreoffice_path = libreoffice_cmd
        # copied from goetenberg, not sure if all are supported
        self.supported_file_extensions = ['.123', '.602', '.abw', '.bib', '.bmp', '.cdr', '.cgm', '.cmx', '.csv',
                                          '.cwk', '.dbf', '.dif', '.doc', '.docm', '.docx', '.dot', '.dotm', '.dotx',
                                          '.dxf', '.emf', '.eps', '.epub', '.fodg', '.fodp', '.fods', '.fodt', '.fopd',
                                          '.gif', '.htm', '.html', '.hwp', '.jpeg', '.jpg', '.key', '.ltx', '.lwp',
                                          '.mcw', '.met', '.mml', '.mw', '.numbers', '.odd', '.odg', '.odm', '.odp',
                                          '.ods', '.odt', '.otg', '.oth', '.otp', '.ots', '.ott', '.pages', '.pbm',
                                          '.pcd', '.pct', '.pcx', '.pdb', '.pdf', '.pgm', '.png', '.pot', '.potm',
                                          '.potx', '.ppm', '.pps', '.ppt', '.pptm', '.pptx', '.psd', '.psw', '.pub',
                                          '.pwp', '.pxl', '.ras', '.rtf', '.sda', '.sdc', '.sdd', '.sdp', '.sdw',
                                          '.sgl', '.slk', '.smf', '.stc', '.std', '.sti', '.stw', '.svg', '.svm',
                                          '.swf', '.sxc', '.sxd', '.sxg', '.sxi', '.sxm', '.sxw', '.tga', '.tif',
                                          '.tiff', '.txt', '.uof', '.uop', '.uos', '.uot', '.vdx', '.vor', '.vsd',
                                          '.vsdm', '.vsdx', '.wb2', '.wk1', '.wks', '.wmf', '.wpd', '.wpg', '.wps',
                                          '.xbm', '.xhtml', '.xls', '.xlsb', '.xlsm', '.xlsx', '.xlt', '.xltm',
                                          '.xltx', '.xlw', '.xml'
                                          ]

    def convert_to_pdf(self, data, filename):

        file_ext = os.path.splitext(filename)[1]
        if file_ext not in self.supported_file_extensions:
            return create_json_err_response(400, f"file extension '{file_ext}' is not supported ({filename}).")

        # create tmp dir for all files
        tmp_dir = tempfile.mktemp()
        _logger.debug(f"creating tmp dir: {tmp_dir}")
        os.mkdir(tmp_dir)

        tmp_file_in_path = os.path.join(tmp_dir, f"tmp{file_ext}")
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
            return create_json_err_response(500, f"could not convert file '{filename}' ({result}).")


def _cleanup(tmp_dir):
    _logger.debug(f"cleanup tmp dir {tmp_dir}")
    # shutil.rmtree(tmp_dir)
