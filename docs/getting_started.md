# Getting Started

Teal has two modes:

- **app mode** will run the teal app. In app mode you can also start up the Locust webui.
- **test mode** will run the tests and print the result to stdout.

## Running Teal in App Mode

Here's a quick example of how easy it is to work with Teal:

```bash
docker run --pull=always --rm -it -p 8000:8000 --name teal ghcr.io/rueedlinger/teal:main
```

Next you can use the api with the openapi ui.

- http://localhost:8000/docs

### Teal REST API Endpoint

#### Extract Text From a PDF

This will extract the text from a digital pdf.

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/pdf/text' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@file.pdf;type=application/pdf'
```

#### Extract Text With OCR From a PDF

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

#### Extract Table From a PPF

Extract tables as json from a digital pdf.

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/pdf/table' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@file.pdf;type=application/pdf'
```

#### Convert PDF To PDF/A With OCR

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

#### Validate PDF/A

Validate an PDF against the PDF/A standard.

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/pdfa/validate' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@file.pdf;type=application/pdf'
```

#### Convert Libreoffice Documents to PDF

Convert a Libreoffice document to PDF.

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/libreoffice/convert' \
  -H 'accept: */*' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@file.docx;type=application/vnd.openxmlformats-officedocument.wordprocessingml.document'
```

### Starting Teal with Locust (Load Testing)

Teal also includes Locust load tests, you just need to set the environment variable `TEAL_START_LOCUST=true`.
The following command will start the Locust web UI inside the Docker container.

```bash
docker run --pull=always --rm -it -p 8089:8089 -p 8000:8000 \
  -e TEAL_START_LOCUST=true --name teal ghcr.io/rueedlinger/teal:main
```

You can now start the load test from the locust webui (http://0.0.0.0:8089/).

## Running Teal in Test Mode

Teal is packed with unit and integration tests, you just need to set the environment varaible `TEAL_TEST_MODE=true`.
These tests can be run and verified with teh following command.

```bash
docker run --pull=always --rm -it -p 8000:8000 \
  -e TEAL_TEST_MODE=true --name teal ghcr.io/rueedlinger/teal:main
```
