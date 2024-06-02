# Home

**Teal** is a versatile and user-friendly API designed to simplify working with PDF documents. Whether you're a
developer looking to automate PDF processing or integrate PDF functionalities into your existing workflow, Teal provides
a seamless and efficient solution.

For the source code, see [https://github.com/rueedlinger/teal](https://github.com/rueedlinger/teal).

## Key Features

- Digitize documents to searchable PDF or archivable PDF/A.
- Extract metadata, text, and tables as structured data.
- Convert different document types to PDF.
- Convert PDFs to PDF/A.
- Check PDF/A compliance.

## Understanding Different Types of PDFs

**Digitally Created PDFs:**

- Created using software like Microsoft Word or Excel, or via the "print" function within applications.
- Contains text and images with electronic character designation.
- Text and images can be easily edited, searched, and manipulated.

**Image-only PDFs:**

- Generated from scanned hard copy documents or images.
- Content is locked in a snapshot-like image without a text layer.
- Not searchable or editable without OCR (Optical Character Recognition).

**Searchable PDFs:**

- Result from applying OCR to scanned or image-based documents.
- Have a text layer added underneath the image layer, making them fully searchable.
- Text can be selected, copied, and marked up like in original documents.

## Libraries and Binaries Used in Teal

**Teal** uses other open-source libraries and provides this functionality through convenient APIs.

**Docker Base Image**

Currently `python:3.12` is used as Docker base image.

**Python Libraries:**

The following python packages are defiend in the `requirements.in`file.

```text
fastapi
prometheus-fastapi-instrumentator
python-multipart
uvicorn
gunicorn
pyyaml
pypdfium2
pytesseract
pdf2image
camelot-py
# needed by camelot-py
ghostscript
# needed by camelot-py
opencv-python
PyPDF2
pytest
pytest-cov
locust
black
```

You can generate the full list of dependencies with `pip-compile` (
see [pip-compile](https://pip-tools.readthedocs.io/en/stable/)).

**Binaries:**

The following binaries (debian packages) are needed:

- tesseract-ocr
- tesseract-ocr-eng (and additional required languages)
- poppler-utils
- ocrmypdf
- ghostscript
- python3-tk
- libgl1
- libreoffice
- default-jre-headless
- libreoffice-java-common
- jodconverter

For more details have a look at the Docker file.
