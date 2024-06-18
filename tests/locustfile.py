import os

from locust import task, FastHttpUser, tag


class TealApiRequest(FastHttpUser):

    DOC_LOAD_TEST = "data/digital_pdf/loadtest.pdf"

    @tag("create_pdf")
    @task
    def libreoffice_convert_pdf(self):
        with open(get_path(self.DOC_LOAD_TEST), "rb") as f:
            response = self.client.post("/create/pdf", files={"file": f})

    @tag("create_doc")
    @task
    def libreoffice_convert_doc(self):
        with open(get_path(self.DOC_LOAD_TEST), "rb") as f:
            response = self.client.post("/create/doc", files={"file": f})

    @tag("validate_pdfa")
    @task
    def pdfa_validate(self):
        with open(get_path(self.DOC_LOAD_TEST), "rb") as f:
            response = self.client.post("/validate/pdfa", files={"file": f})

    @tag("ocr_pdf")
    @task
    def pdfa_convert(self):
        with open(get_path(self.DOC_LOAD_TEST), "rb") as f:
            response = self.client.post("/ocr/pdf", files={"file": f})

    @tag("extract_text")
    @task
    def pdf_text(self):
        with open(get_path(self.DOC_LOAD_TEST), "rb") as f:
            response = self.client.post("/extract/text", files={"file": f})

    @tag("extract_meta")
    @task
    def pdf_ocr(self):
        with open(get_path(self.DOC_LOAD_TEST), "rb") as f:
            response = self.client.post("/extract/meta", files={"file": f})

    @tag("extract_table")
    @task
    def pdf_table(self):
        with open(get_path(self.DOC_LOAD_TEST), "rb") as f:
            response = self.client.post("/extract/table", files={"file": f})


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
