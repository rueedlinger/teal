# Releases

All available releases are listed here:

- [https://github.com/rueedlinger/teal/releases](https://github.com/rueedlinger/teal/releases)

## Versions

| Version                    | Docker                                              | Description                                                                                   |
|----------------------------|-----------------------------------------------------|-----------------------------------------------------------------------------------------------|
| `main`                     | `ghcr.io/rueedlinger/teal:main`                     | main branch version                                                                           |
| `latest`                   | `ghcr.io/rueedlinger/latest:main`                   | Latest release                                                                                |
| `v{MAJOR}.{MINOR}.{PATCH}` | `ghcr.io/rueedlinger/teal:v{MAJOR}.{MINOR}.{PATCH}` | For a full list of releases see [Teal releases](https://github.com/rueedlinger/teal/releases) |

These are the available releases and their corresponding Docker images for the 'teal' project.

## Libraries and Binaries Used in Teal

**Teal** uses other open-source libraries and provides this functionality through convenient APIs.

A list of used libraries and brines can be queried over the `/app/info` endpoint.

```bash
curl localhost:8000/app/info
```

**Docker Base Image**

Currently `python:3.12` is used as Docker base image.

**Python Libraries:**

The following python packages are defined in
the [requirements.in](https://github.com/rueedlinger/teal/blob/main/requirements.in) file.

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
see [pip-compile](https://pip-tools.readthedocs.io/en/stable/)). This will generate
the [requirements.txt](https://github.com/rueedlinger/teal/blob/main/requirements.txt) with all
dependencies.

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
- libreoffice-java-common
- default-jre-headless

For more details have a look at the [Dockerfile](https://github.com/rueedlinger/teal/blob/main/Dockerfile).

## Known Issues

### Extract Tables (/pdf/table ) - Ignoring wrong pointing object

The following warning is displayed when extracting tables from a PDF. The extraction works, but this warning is
displayed:

```
pypdf._reader - WARNING - Ignoring wrong pointing object 6 0 (offset 0)
```

This warning typically indicates that the PyPDF library encountered an object in the PDF that it couldn't interpret
correctly. Despite this, the extraction process completes successfully. This warning may not impact the extracted data
but suggests that there might be some issues with the PDF's structure or content.

### Metrics - CPU and MEM metrics not available with multiworker

This is unrelated to trallnag/prometheus-fastapi-instrumentator. The official Prometheus client library for Python does
not include these metrics when multi process mode is enabled.

see [https://github.com/trallnag/prometheus-fastapi-instrumentator/issues/207](https://github.com/trallnag/prometheus-fastapi-instrumentator/issues/207)