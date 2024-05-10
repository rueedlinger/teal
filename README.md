# xfy - extract structured data from pdf files

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
