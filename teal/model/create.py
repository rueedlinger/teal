from enum import Enum


class OutputType(str, Enum):
    PDFA_1B = "pdfa-1b"
    PDFA_2B = "pdfa-2b"
    PDFA_3B = "pdfa-3b"
    PDF_15 = "pdf-1.5"
    PDF_16 = "pdf-1.6"
    PDF_17 = "pdf-1.7"

    def to_param(self):
        if self.value == self.PDFA_1B.value:
            return "1"
        elif self.value == self.PDFA_2B.value:
            return "2"
        elif self.value == self.PDFA_3B.value:
            return "3"
        elif self.value == self.PDF_15.value:
            return "15"
        elif self.value == self.PDF_16.value:
            return "16"
        elif self.value == self.PDF_17.value:
            return "17"
        else:
            return "0"
