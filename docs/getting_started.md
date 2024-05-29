# Getting Started

Teal has two modes:

- **app mode** will run the teal app.
- **test mode** will run the tests and print the result to stdout.

## Running Teal in App Mode

Here's a quick example of how easy it is to work with Teal:

```bash
docker run --rm -it -p 8000:8000 --name teal ghcr.io/rueedlinger/teal:main
```

Next you can use the api with the openapi ui.

- http://localhost:8000/docs

### Extract Text From a PDF

This will extract the text from a digital pdf.

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/pdf/text' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@file.pdf;type=application/pdf'
```

### Extract Text With OCR From a PDF

Extract text from a image only pdf with default languages (eng).

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/pdf/ocr' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@file.pdf;type=application/pdf'
```

Extract text from a image only pdf with multiple languages (eng, deu). The languages correspond to the tesseract
languages codes.

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/pdf/ocr?languages=eng&languages=deu' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@file.pdf;type=application/pdf'
```

### Extract Table From a PPF

Extract tables as json from a digital pdf.

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/pdf/table' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@file.pdf;type=application/pdf'
```

### Convert PDF To PDF/A With OCR

Convert a PDF to PDF/A. If the PDF is a scanned image, OCR is used with default languages eng. The languages correspond
to the tesseract languages codes.

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/pdfa/convert' \
  -H 'accept: */*' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@file.pdf;type=application/pdf'
```

Convert a PDF to PDF/A. If the PDF is a scanned image, OCR is used with the languages eng and deu. The default is
PDF/A-1.

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/pdfa/convert?languages=eng&languages=deu' \
  -H 'accept: */*' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@file.pdf;type=application/pdf'
```

The following converts to PDF/A-3.

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/pdfa/convert?pdfa=pdfa-3' \
  -H 'accept: */*' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@file.pdf;type=application/pdf'
```

### Validate PDF/A

Validate an PDF against the PDF/A standard.

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/pdfa/validate' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@file.pdf;type=application/pdf'
```

### Convert Libreoffice Documents to PDF

Convert a Libreoffice document to PDF.

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/libreoffice/convert' \
  -H 'accept: */*' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@file.docx;type=application/vnd.openxmlformats-officedocument.wordprocessingml.document'
```

## Running Teal in Test Mode

Teal is packed with unit and integration tests. These tests can be run and verified with teh following command.

```bash
docker run --rm -it -p 8000:8000 -e TEAL_TEST_MODE=true --name teal ghcr.io/rueedlinger/teal:main
```
