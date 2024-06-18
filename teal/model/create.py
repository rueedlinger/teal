from enum import Enum


class DocOutputType(str, Enum):
    ODT = "odt"
    DOC = "doc"
    DOCX = "docx"

    def to_file_ext(self):
        return f".{self.value}"


class PdfOutputType(str, Enum):
    PDFA_1B = "pdfa-1b"
    PDFA_2B = "pdfa-2b"
    PDFA_3B = "pdfa-3b"
    PDF_15 = "pdf-1.5"
    PDF_16 = "pdf-1.6"
    PDF_17 = "pdf-1.7"

    def to_param(self):
        if self.name == self.PDFA_1B.name:
            return "1"
        elif self.name == self.PDFA_2B.name:
            return "2"
        elif self.name == self.PDFA_3B.name:
            return "3"
        elif self.name == self.PDF_15.name:
            return "15"
        elif self.name == self.PDF_16.name:
            return "16"
        elif self.name == self.PDF_17.name:
            return "17"
        else:
            return "0"
