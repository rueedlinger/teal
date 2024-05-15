# teal - a convenient REST API for working with PDF's

**teal** aims to provide a user-friendly API for working with PDFs which can be easily integrated in an existing
workflow. The main features are:

- Digitalized documents to searchable or achievable PDF (PDF/A) .
- Extract meta data, text and tables as structured data.
- Convert different documents types to PDF.

**teal** uses other open source libraries and provide these functionally as convince API.

| Feature                                           | Library                 |
|---------------------------------------------------|-------------------------|
| Extract text from PDFs                            | pypdfium2               |
| Extract text from scanned PDFs (OCR)              | pytesseract             |
| Extract tables from PDFs                          | camelot                 |
| Convert PDF to PDF/A (with OCR when no text)      | ocrmypdf                |
| Convert Office documents to PDF                   | libreoffice             |
| Extract meta data from PDF                        | **not yet implemented** |
| Process documents from a remote repository (HTTP) | **not yet implemented** |

> **Note:** At the moment this version is not optimized and tested in production. Any feedback is welcomed.

## Docker

| ENV           | Default       | Description                     |
|---------------|---------------|---------------------------------|
| TEAL_LOG_CONF | log_conf.yaml | The python logging conf (yaml)  |
| TEAL_WORKERS  | 1             | The number of worker processes. |
| TEAL_PORT     | 8000          | Bind socket to this port        |
| TEAL_IP_BIND  | 0.0.0.0       | Bind socket to this host.       |

### Feature flags

You can disable different features in teal with the env `TEA_FEATURE_<PATH>`. For example to disable the libreoffice
feature (`/convert/libreoffice`) you can set `TEA_FEATURE_CONVERT_LIBREOFFICE=false`.

## API

- OpenAPI http://127.0.0.1:8000/docs
- Redoc http://127.0.0.1:8000/redoc

## Development Setup

### Python

```bash
pyenv install 3.12.0 
pyenv virtualenv 3.12.0 teal 
pyenv activate teal  
pip install -r requiremnts.txt
```

```bash
uvicorn teal.api:app --reload
```

### Docker Container

To start up the whole app just build and run the container with `docker compose`.

```bash
docker compose up --build
```

### Testing

To run the pytest inside the docker container just pass the env `TEAL_TEST_MODE=true`. When you want to pass
arguments to pytest you can use the env `TEAL_PYTEST_ARGS`.

```bash
docker compose run --build --name teal_pytest --rm -e TEAL_TEST_MODE=true teal
```

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


