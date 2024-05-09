import io
import json
import logging
import tempfile

from starlette.responses import JSONResponse

from xdractify.model import TextExtract, TableExtract

_ACTION_TEXT = "text"
_ACTION_TABLE = "table"
_ENGINE_PDFIUM = "pdfium"
_ENGINE_PYPDF = "pypdf"
_ENGINE_TESSERACT = "tesseract"
_ENGINE_CAMELOT = "camelot"

_logger = logging.getLogger("xdractify.pdf")


def extract_text_tesseract(data, params):
    from pdf2image import convert_from_bytes
    import pytesseract

    extracts = []
    images = convert_from_bytes(data)
    _logger.debug(f"found images {len(images)} with pdf2images")
    lang = None
    if "lang" in params:
        lang = params["lang"]
    _logger.debug(f"using lang {len(lang)} with pytesseract")

    for i, page in enumerate(images):
        text = pytesseract.image_to_string(page, lang=lang)
        extracts.append(TextExtract.parse_obj({"text": text, "page": i}))
    return extracts


def extract_text_pypdf(data, params):
    from pypdf import PdfReader

    extracts = []
    reader = PdfReader(io.BytesIO(data))
    _logger.debug(f"found {len(reader.pages)} pages with pypdf")
    for p in range(len(reader.pages)):
        page = reader.pages[p]
        text = page.extract_text()
        extracts.append(TextExtract.parse_obj({"text": text, "page": p}))
    return extracts


def extract_text_pypdfium(data, params):
    import pypdfium2 as pdfium

    extracts = []
    pdf = pdfium.PdfDocument(data)
    _logger.debug(f"found {len(pdf)} pages with pdf")
    for p in range(len(pdf)):
        textpage = pdf[p].get_textpage()
        text_all = textpage.get_text_bounded()
        extracts.append(TextExtract.parse_obj({"text": text_all, "page": p}))

    return extracts


def extract_table(data, params):
    import camelot.io as camelot

    with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp_pdf_file:
        tmp_pdf_file.write(data)
        tables = camelot.read_pdf(tmp_pdf_file.name)
        _logger.debug(f"found {len(tables)} tables with camelot")
        extracts = []

        for p in range(len(tables)):
            with tempfile.NamedTemporaryFile(suffix=".json") as tmp_json_file:
                tables[p].to_json(tmp_json_file.name)
                f = open(tmp_json_file.name)
                table_json = json.load(f)
                extracts.append(
                    TableExtract.parse_obj({"index": p, "table": table_json})
                )
                f.close()

    return extracts


class PdfModule:

    def __init__(self):

        self.modules = {
            (_ENGINE_PDFIUM, _ACTION_TEXT): extract_text_pypdfium,
            (_ENGINE_PYPDF, _ACTION_TEXT): extract_text_pypdf,
            (_ENGINE_TESSERACT, _ACTION_TEXT): extract_text_tesseract,
            (_ENGINE_CAMELOT, _ACTION_TABLE): extract_table,
        }

    def run(self, module, action, data, params):
        _logger.debug(f"module: {module}, action: {action}, params: {params}")
        if (module, action) in self.modules:
            return self.modules[(module, action)](data, params)
        else:
            return JSONResponse(
                status_code=400,
                content={
                    "message": f"module {module} and action ${action} is not supported"
                },
            )

    def get_modules(self):
        return self.modules.keys()
