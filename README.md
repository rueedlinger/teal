# teal - a convenient REST API for working with PDF's

**teal** aims to provide a user-friendly API for working with PDFs which can be easily integrated in an existing
workflow. The main features are:

- Digitalized documents to searchable or achievable PDF (PDF/A) .
- Extract meta data, text and tables as structured data.

<span style="color:blue">some *blue* text</span>.

*teal* uses other open source libraries and provide these functionally as convince API.

| Feature                                   | Library     |
|-------------------------------------------|-------------|
| Extract text                              | pdfium      |
| Extract text from scanned documents (OCR) | pytesseract |
| Extract tables                            | camelot     |
| Extract meta data                         | pikepdf     |

## Setup

### Docker

```bash
docker compose build
```

```bash
docker comppose up
```

### Python

```bash
pyenv install 3.12.0 
pyenv virtualenv 3.12.0 xtra 
pyenv activate xtra  
pip install -r requiremnts.txt
```

```bash
uvicorn xtra.api:app --reload
```

## API

- OpenAPI http://127.0.0.1:8000/docs
- Redoc, http://127.0.0.1:8000/redoc

mac
brew install poppler (pdf2image)
brew install tesseract
brew install tesseract-lang
brew install ghostscript tcl-tk (camelot)

## Understanding Different Types of PDFs

Digitally created PDFs:

- Created using software like Microsoft Word or Excel, or via the "print" function within applications.
- Contains text and images with electronic character designation.
- Text and images can be easily edited, searched, and manipulated.

Image-only PDFs:

- Generated from scanned hard copy documents or images.
- Content is locked in a snapshot-like image without a text layer.
- Not searchable or editable without OCR (Optical Character Recognition).

Searchable PDFs:

- Result from applying OCR to scanned or image-based documents.
- Have a text layer added underneath the image layer, making them fully searchable.
- Text can be selected, copied, and marked up like in original documents.


