import os

from locust import task, FastHttpUser, tag


class TealApiRequest(FastHttpUser):

    DOC_LOAD_TEST = "data/digital_pdf/loadtest.pdf"

    @tag("libreoffice_convert")
    @task
    def libreoffice_convert(self):
        with open(get_path(self.DOC_LOAD_TEST), "rb") as f:
            response = self.client.post("/libreoffice/convert", files={"file": f})

    @tag("pdfa_validate")
    @task
    def pdfa_validate(self):
        with open(get_path(self.DOC_LOAD_TEST), "rb") as f:
            response = self.client.post("/pdfa/validate", files={"file": f})

    @tag("pdfa_convert")
    @task
    def pdfa_convert(self):
        with open(get_path(self.DOC_LOAD_TEST), "rb") as f:
            response = self.client.post("/pdfa/convert", files={"file": f})

    @tag("pdf_text")
    @task
    def pdf_text(self):
        with open(get_path(self.DOC_LOAD_TEST), "rb") as f:
            response = self.client.post("/pdf/text", files={"file": f})

    @tag("pdf_ocr")
    @task
    def pdf_ocr(self):
        with open(get_path(self.DOC_LOAD_TEST), "rb") as f:
            response = self.client.post("/pdf/ocr", files={"file": f})

    @tag("pdf_table")
    @task
    def pdf_table(self):
        with open(get_path(self.DOC_LOAD_TEST), "rb") as f:
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
