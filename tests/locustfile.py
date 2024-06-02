import os

from locust import task, FastHttpUser, tag


class TealApiRequest(FastHttpUser):

    @tag("libreoffice_convert")
    @task
    def libreoffice_convert(self):
        with open(get_path("data/doc/word_document.docx"), "rb") as f:
            response = self.client.post("/libreoffice/convert", files={"file": f})

    @tag("pdfa_validate")
    @task
    def pdfa_validate(self):
        with open(get_path("data/pdfa/pdfa_2b.pdf"), "rb") as f:
            response = self.client.post("/pdfa/validate", files={"file": f})

    @tag("pdfa_convert")
    @task
    def pdfa_convert(self):
        with open(get_path("data/digital_pdf/document_two_pages.pdf"), "rb") as f:
            response = self.client.post("/pdfa/convert", files={"file": f})

    @tag("pdf_text")
    @task
    def pdf_text(self):
        with open(get_path("data/digital_pdf/document_two_pages.pdf"), "rb") as f:
            response = self.client.post("/pdf/text", files={"file": f})

    @tag("pdf_ocr")
    @task
    def pdf_ocr(self):
        with open(get_path("data/ocr/scanned_document.pdf"), "rb") as f:
            response = self.client.post("/pdf/ocr", files={"file": f})

    @tag("pdf_table")
    @task
    def pdf_table(self):
        with open(get_path("data/digital_pdf/document_with_one_table.pdf"), "rb") as f:
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
