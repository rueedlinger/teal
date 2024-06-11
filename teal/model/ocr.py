from enum import Enum


class OutputType(str, Enum):
    PDFA_1B = "pdfa-1b"
    PDFA_2B = "pdfa-2b"
    PDFA_3B = "pdfa-3b"
    PDF = "pdf"

    def to_param(self):
        if self.value == self.PDFA_1B:
            return "pdfa-1"
        elif self.value == self.PDFA_2B:
            return "pdfa-2"
        elif self.value == self.PDFA_3B:
            return "pdfa-3"
        else:
            return "pdf"


class OcrMode(str, Enum):
    SKIP_TEXT = "skip-text"
    FORCE_OCR = "force-ocr"
    REDO_OCR = "redo-ocr"

    def to_param(self):
        if self.value is None:
            return "--skip-text"
        else:
            return f"--{self.value}"
