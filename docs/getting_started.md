# Getting Started

Teal has two modes:

- **APP mode** will run the teal app. In app mode you can also start up the Locust webui.
- **TEST mode** will run the tests and print the result to stdout.

## Running Teal in App Mode

Here's a quick example of how easy it is to work with Teal:

```bash
docker run --pull=always --rm -it -p 8000:8000 \
  --name teal ghcr.io/rueedlinger/teal:latest
```

Next you can use the api with the openapi ui.

- [http://localhost:8000/docs](http://localhost:8000/docs)

## Examples

### Extract Text From a PDF

This endpoint will extract the text from a digital PDF.

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/pdf/text' \
  -F 'file=@../tests/data/digital_pdf/loadtest.pdf;type=application/pdf'
```

The response might look like this:

```json
[
  {
    "page": 1,
    "text": "Lorem ipsum"
  }
]
```

### Extract Text With OCR From a PDF

This endpoint extracts text from an image-only PDF or a digital PDF using the default language (English).

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/pdf/ocr?languages=eng' \
  -F 'file=@../tests/data/ocr/scanned_document.pdf'
```

The extracted text from the PDF might look like the following response:

```json
[
  {
    "page": 1,
    "text": "Lorem ipsum"
  }
] 
```

### Extract Table From a PDF

This endpoint extracts tables as JSON from a digital PDF.

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/pdf/table' \
  -F 'file=@../tests/data/digital_pdf/document_with_one_table.pdf'
```

The response might look like this:

```json
[
  {
    "page": 1,
    "index": 0,
    "table": [
      {
        "0": "A",
        "1": "B",
        "2": "C"
      },
      {
        "0": "A1",
        "1": "B11",
        "2": "C111"
      },
      {
        "0": "A2",
        "1": "B22",
        "2": "C222"
      },
      {
        "0": "A3",
        "1": "B33",
        "2": "C333"
      }
    ]
  }
]%
```

### Extract Metadata From a PDF

This endpoint extracts metadata from a PDF.

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/pdf/meta' \
  -F 'file=@../tests/data/digital_pdf/loadtest.pdf'
```

The extracted metadata from the PDF might look like the following response:

```json
{
  "fileName": "loadtest.pdf",
  "fileSize": 16873,
  "pdfVersion": "1.3",
  "pdfaClaim": null,
  "pages": 1,
  "docInfo": {
    "/Author": "foo",
    "/CreationDate": "D:20240602153930Z00'00'",
    "/Creator": "Word",
    "/ModDate": "D:20240602153930Z00'00'",
    "/Producer": "macOS Version 14.5 (Build 23F79) Quartz PDFContext",
    "/Title": "Document1"
  },
  "xmp": {}
}
```

### Convert PDF To PDF/A With OCR

This endpoint converts a PDF to PDF/A. If the PDF is a scanned image, OCR is used with the default language (English).
The languages correspond to the Tesseract language codes.

```bash
curl -X 'POST' --output pdfa.pdf \
  'http://127.0.0.1:8000/pdfa//convert?languages=enf&?pdfa=pdfa-3' \
  -F 'file=@../tests/data/digital_pdf/loadtest.pdf'
```

The output is a PDF/A file.

### Validate PDF/A

This endpoint validates a PDF against the PDF/A standard.

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/pdfa/validate' \
  -F 'file=@../tests/data/pdfa/pdfa_2b.pdf'
```

This will generate an output like this:

```json
{
  "profile": "PDF/A-2B",
  "statement": "PDF file is compliant with Validation Profile requirements.",
  "compliant": true,
  "details": {
    "passedRules": 143,
    "failedRules": 0,
    "passedChecks": 400,
    "failedChecks": 0,
    "ruleSummaries": []
  }
}
```

### Convert LibreOffice Documents to PDF

This endpoint converts a LibreOffice document to PDF (version 1.6).

```bash
curl -X 'POST' --output pdf.pdf \
  'http://127.0.0.1:8000/libreoffice/convert?profile=pdf-1.6' \
  -F 'file=@../tests/data/doc/text_document.txt'
```

The output is a PDF document.

## Running Teal in Test Mode

Teal is packed with unit and integration tests, you just need to set the environment varaible `TEAL_TEST_MODE=true`.
These tests can be run and verified with teh following command.

```bash
docker run --pull=always --rm -it -p 8000:8000 \
  -e TEAL_TEST_MODE=true --name teal ghcr.io/rueedlinger/teal:latest
```

## Starting Teal with Locust (Load Testing)

Teal also includes Locust load tests, you just need to set the environment variable `TEAL_START_LOCUST=true`.
The following command will start the Locust web UI inside the Docker container.

```bash
docker run --pull=always --rm -it -p 8089:8089 -p 8000:8000 \
  -e TEAL_START_LOCUST=true --name teal ghcr.io/rueedlinger/teal:latest
```

You can now start the load test from the locust webui [http://localhost:8089/](http://localhost:8089/).

