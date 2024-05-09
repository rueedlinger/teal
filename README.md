# xtractify

## Setup

```bash
pyenv install 3.12.0 
pyenv virtualenv 3.12.0 xdractify 
pyenv activate xdractify  
```

```bash
uvicorn xdractify.api:app --reload --log-config=log_conf.yaml
```

http://127.0.0.1:8000/
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc

mac
brew install poppler (pdf2image)
brew install tesseract
brew install tesseract-lang
brew install ghostscript tcl-tk (camelot)
