# Getting Started

Teal has two modes:

- **app mode** will run the teal app.
- **test mode** will run the tests and print the result to stdout.

## Running Teal in App Mode

Here's a quick example of how easy it is to work with Teal:

```bash
docker run --rm -it -p 8000:8000 --name teal ghcr.io/rueedlinger/teal:latest
```

Next you can use the api with the openapi ui.

- http://127.0.0.1:8000/docs

### Extract Text From a PDF

```bash
curl -X 'POST' \
  'http://0.0.0.0:8000/pdf/text' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@file.pdf;type=application/pdf'
```

### Extract Text With OCR From a PDF

```bash
curl -X 'POST' \
  'http://0.0.0.0:8000/pdf/ocr' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@file.pdf;type=application/pdf'
```

### Extract Table From a PPF

```bash
curl -X 'POST' \
  'http://0.0.0.0:8000/pdf/table' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@file.pdf;type=application/pdf'
```

### Convert PDF To PDF/A With OCR

```bash
curl -X 'POST' \
  'http://0.0.0.0:8000/pdfa/convert' \
  -H 'accept: */*' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@fileE.pdf;type=application/pdf'
```

### Validate PDF/A

```bash
curl -X 'POST' \
  'http://0.0.0.0:8000/pdfa/validate' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@file.pdf;type=application/pdf'
```

### Convert Libreoffice Documents to PDF

```bash
curl -X 'POST' \
  'http://0.0.0.0:8000/libreoffice/convert' \
  -H 'accept: */*' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@file.pdf;type=application/pdf'
```

## Running Teal in Test Mode

Teal is packed with unit and integration tests. These tests can be run and verified with teh following command.

```bash
docker run --rm -it -p 8000:8000 -e TEAL_TEST_MODE=true --name teal ghcr.io/rueedlinger/teal:latest
```
