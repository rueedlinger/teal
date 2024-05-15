import os


def load_file(file):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, file)
    pdf_file = open(filename, "rb")
    data = pdf_file.read()
    pdf_file.close()
    return data
