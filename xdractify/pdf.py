import io

from xdractify.model import Extracts, TextExtract

_ACTION_EXTRACT = "extract"
_ENGINE_PDFIUM = "pdfium"
_ENGINE_PYPDF = "pypdf"


def extract_pypdf(data):
    from pypdf import PdfReader

    extracts = []
    reader = PdfReader(io.BytesIO(data))
    for p in range(len(reader.pages)):
        page = reader.pages[p]
        text = page.extract_text()
        extracts.append(TextExtract.parse_obj({"text": text, "page": p}))
    return Extracts.parse_obj({"extracted_text": extracts})


def extract_pypdfium2(data):
    import pypdfium2 as pdfium

    extracts = []
    pdf = pdfium.PdfDocument(data)
    for p in range(len(pdf)):
        textpage = pdf[p].get_textpage()
        text_all = textpage.get_text_bounded()
        extracts.append(TextExtract.parse_obj({"text": text_all, "page": p}))

    return Extracts.parse_obj({"extracted_text": extracts})


class PdfModule:

    def __int__(self):
        self.modules = {(_ENGINE_PDFIUM, _ACTION_EXTRACT): extract_pypdfium2}
