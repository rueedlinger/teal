# REST API

## PDF

* Extracts text from a digital PDF.
* Extracts text from an image-only PDF or a digital PDF using OCR.
* Extracts tables as JSON from a digital PDF.
* Extracts metadata from a PDF.

### /pdf/text

This multipart/form-data route extracts text from a digital PDF.

```
POST /pdf/text
```

**Form Filed (multipart/form-data)**

| Key  | Description                         |
|------|-------------------------------------|
| file | The PDF from which to extract text. |

**Query Parameters**

| Parameter | Type            | Values                                                  | Description          |
|-----------|-----------------|---------------------------------------------------------|----------------------|
| pages     | `Array[String]` | selection `1,2,3` or ranges `1-8` or combined `1,2,5-6` | The pages to extract |

**Examples**

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/pdf/text?pages=1' \
  -F 'file=@../tests/data/digital_pdf/loadtest.pdf' 
```

### /pdf/ocr

This multipart/form-data route extracts text with OCR from a scanned or digital PDF.

```
POST /pdf/ocr
```

**Form Filed (multipart/form-data)**

| Key  | Description                         |
|------|-------------------------------------|
| file | The PDF from which to extract text. |

**Query Parameters**

| Parameter | Type            | Values                                                   | Description                                              |
|-----------|-----------------|----------------------------------------------------------|----------------------------------------------------------|
| pages     | `String`        | selection `1,2,3` or  ranges `1-8` or combined `1,2,5-6` | The pages to extract                                     |
| languages | `Array[String]` | `eng, fra, deu, ...`                                     | The tesseract languages used for the OCR text extraction |

**Examples**

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/pdf/ocr?pages=1&languages=deu&languages=eng' \
  -F 'file=@../tests/data/digital_pdf/loadtest.pdf' 
```

### /pdf/table

This multipart/form-data route extracts tables from a digital PDF.

```
POST /pdf/table
```

**Form Filed (multipart/form-data)**

| Key  | Description                         |
|------|-------------------------------------|
| file | The PDF from which to extract text. |

**Query Parameters**

| Parameter | Type     | Values                                                   | Description          |
|-----------|----------|----------------------------------------------------------|----------------------|
| pages     | `String` | selection `1,2,3` or  ranges `1-8` or combined `1,2,5-6` | The pages to extract |

**Examples**

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/pdf/table?pages=1' \
  -F 'file=@../tests/data/digital_pdf/document_with_one_table.pdf' 
```

### /pdf/meta

This multipart/form-data route extracts metadata (docinfo & xmp) from a PDF.

```
POST /pdf/meta
```

**Form Filed (multipart/form-data)**

| Key  | Description                         |
|------|-------------------------------------|
| file | The PDF from which to extract text. |

## PDF/A

* Converts a PDF to PDF/A (PDF/A-1B, PDF/A-2B or PDF/A-3B) with OCR.
* Validates a PDF against the PDF/A standard.

**Examples**

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/pdf/meta' \
  -F 'file=@../tests/data/digital_pdf/loadtest.pdf' 
```

### /pdfa/convert

This multipart/form-data route converts a PDF to PDF/A.

```
POST /pdfa/convert
```

**Form Filed (multipart/form-data)**

| Key  | Description                         |
|------|-------------------------------------|
| file | The PDF from which to extract text. |

**Query Parameters**

| Parameter | Type            | Values                                                   | Description                                                                                                                                                                                                                                  |
|-----------|-----------------|----------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| pages     | `String`        | selection `1,2,3` or  ranges `1-8` or combined `1,2,5-6` | The pages to extract                                                                                                                                                                                                                         |
| languages | `Array[String]` | `eng, fra, deu, ...`                                     | The tesseract languages used for the OCR text extraction                                                                                                                                                                                     |
| ocr       | `Enum`          | `skip-text, force-ocr, redo-ocr`                         | `skip-text` will not run OCR on pages with text. `foce-ocr` will run OCR on all pages. `redo-ocr` will categorized text as either visible or invisible.  Invisible text (OCR) is stripped out and and any additional text is inserted as OCR |
| profile   | `Enum`          | `pdfa-1b, pdfa-2b, pdfa-3b`                              | The profile to export to.                                                                                                                                                                                                                    |

**Examples**

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/pdfa/convert?pages=1&languages=eng&ocr=skip-text&profile=pdfa-3b' \
  -F 'file=@../tests/data/digital_pdf/loadtest.pdf' \
  -o pdfa.pdf
```

### /pdfa/validate

This multipart/form-data route validates a PDF against different PDF/A profiles.

```
POST /pdfa/validate
```

**Form Filed (multipart/form-data)**

| Key  | Description                                      |
|------|--------------------------------------------------|
| file | The PDF to validate against the PDF/A profiles.. |

**Query Parameters**

| Parameter | Type   | Values                                            | Description |
|-----------|--------|---------------------------------------------------|-------------|
| profile   | `Enum` | `1a, 1b, 2a, 2b, 3a, 3b, 3u, 4, 4e, 4f, ua1, ua2` |             |

**Examples**

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/pdfa/validate?profile=3b' \
  -F 'file=@../tests/data/digital_pdf/loadtest.pdf'
```

## LibreOffice

* Converts a LibreOffice document to PDF (supported profiles: PDF 1.5, PDF 1.6, PDF 1.7,
  PDF/A-1B, PDF/A-2B or PDF/A-3B).

### /libreoffice/convert

This multipart/form-data route validates a PDF against different PDF/A profiles.

```
POST /libreoffice/convert
```

**Form Filed (multipart/form-data)**

| Key  | Description                              |
|------|------------------------------------------|
| file | The document to convert to pDF or PDF/A. |

**Query Parameters**

| Parameter | Type     | Values                                                   | Description                            |
|-----------|----------|----------------------------------------------------------|----------------------------------------|
| pages     | `String` | selection `1,2,3` or  ranges `1-8` or combined `1,2,5-6` | The pages to extract                   |
| profile   | `Enum`   | `pdfa-1b, pdfa-2b, pdfa-3b, pdf-1.5, pdf-1.6, pdf-1.7`   | The profile teh document to convert to |

**Examples**

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/libreoffice/convert?profile=pdf-1.6' \
  -F 'file=@../tests/data/doc/text_document.txt' \
  -o mypdf.pdf
```
