import os

from locust import task, FastHttpUser


class TealApiRequest(FastHttpUser):
    @task
    def run_all_requests_in_order(self):
        # pdf
        self.pdf_ocr()
        self.pdf_table()
        self.pdf_text()
        # libreoffice
        self.libreoffice_convert()
        # pdfa
        self.pdfa_convert()
        self.pdfa_validate()

    def libreoffice_convert(self):
        with open(get_path("data/doc/normal_document.docx"), "rb") as f:
            response = self.client.post("/libreoffice/convert", files={"file": f})

    def pdfa_validate(self):
        with open(get_path("data/pdfa/pdfa_2b.pdf"), "rb") as f:
            response = self.client.post("/pdfa/validate", files={"file": f})

    def pdfa_convert(self):
        with open(get_path("data/digital_pdf/normal_document.pdf"), "rb") as f:
            response = self.client.post("/pdfa/convert", files={"file": f})

    def pdf_text(self):
        with open(get_path("data/digital_pdf/normal_document.pdf"), "rb") as f:
            response = self.client.post("/pdf/text", files={"file": f})

    def pdf_ocr(self):
        with open(get_path("data/ocr/scanned_document.pdf"), "rb") as f:
            response = self.client.post("/pdf/ocr", files={"file": f})

    def pdf_table(self):
        with open(get_path("data/digital_pdf/simple_tables.pdf"), "rb") as f:
            response = self.client.post("/pdf/table", files={"file": f})


def load_file(file):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, file)
    pdf_file = open(filename, "rb")
    data = pdf_file.read()
    pdf_file.close()
    return data


def get_path(file):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, file)
    return filename
