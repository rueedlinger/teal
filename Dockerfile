FROM python:3.12

WORKDIR /usr/src/app

RUN apt-get update
RUN apt-get install -y tesseract-ocr
RUN apt-get install -y tesseract-ocr-deu
RUN apt-get install -y tesseract-ocr-fra
RUN apt-get install -y tesseract-ocr-ita
# pdf2image
RUN apt-get install -y poppler-utils
# camelot
RUN apt-get install -y ghostscript python3-tk
# opencv
RUN apt-get install -y libgl1



COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY log_conf.yaml ./

RUN mkdir /usr/src/app/xdractify
COPY xdractify ./xdractify

CMD ["uvicorn",  "xdractify.api:app", "--log-config=log_conf.yaml", "--host", "0.0.0.0"]