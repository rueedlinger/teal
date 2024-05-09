_ACTION_EXTRACT = "extract"
_ENGINE_TESSERACT = "tesseract"


def extract_tesseract(data):
    pass
    """
    extracts = []
    text = pytesseract.image_to_string(data, lang="en")
    extracts.append(TextExtract.parse_obj({"text": text, "page": i}))
    return Extracts.parse_obj({"extracted_text": extracts})
    """


class OcrModule:

    def __int__(self):
        self.modules = {(_ENGINE_TESSERACT, _ACTION_EXTRACT): extract_pypdfium2}
