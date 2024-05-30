ARG PYTHON_VERSION=3.12
FROM python:$PYTHON_VERSION

ARG USERNAME=worker
ARG USER_UID=1000
ARG USER_GID=$USER_UID
ARG VERSION
ARG TESSERACT_LANGUAGES="tesseract-ocr-deu tesseract-ocr-fra tesseract-ocr-ita tesseract-ocr-eng tesseract-ocr-por tesseract-ocr-spa"

LABEL org.opencontainers.image.title="teal" \
      org.opencontainers.image.description="A convenient REST API for working with PDF's." \
      org.opencontainers.image.documentation="https://teal.yax.ch/" \
      org.opencontainers.image.source="https://github.com/rueedlinger/teal"

WORKDIR /usr/src/app

# supported tesseract languages https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html
RUN groupadd --gid $USER_GID $USERNAME &&\
    useradd --uid $USER_UID --gid $USER_GID -m $USERNAME && \
    wget -O /usr/local/bin/dumb-init https://github.com/Yelp/dumb-init/releases/download/v1.2.5/dumb-init_1.2.5_x86_64  &&\
    chmod +x /usr/local/bin/dumb-init && \
    apt-get update && \
    apt-get install -y tesseract-ocr && \
    apt-get install -y $TESSERACT_LANGUAGES && \
    apt-get install -y poppler-utils && \
    apt-get install -y ghostscript python3-tk && \
    apt-get install -y libgl1 && \
    apt-get install -y ocrmypdf && \
    apt-get --no-install-recommends install -y libreoffice && \
    apt-get install -y default-jre-headless libreoffice-java-common jodconverter

# verapdf
COPY dist/auto-install.xml /tmp
RUN wget -O /tmp/verapdf-installer.zip https://software.verapdf.org/releases/verapdf-installer.zip && \
    unzip -d /tmp /tmp/verapdf-installer.zip && \
    /tmp/verapdf-greenfield-1.26.2/verapdf-install /tmp/auto-install.xml && \
    rm -rf /tmp/verapdf*  && \
    rm -rf /tmp/auto-install.xml

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY dist/log_conf.yaml ./
COPY dist/run.sh ./
RUN chmod a+x run.sh

COPY teal ./teal
COPY tests ./tests

ENV PATH="${PATH}:/usr/local/verapdf"

USER $USERNAME
ENV TEAL_VERSION="$VERSION"
ENV TESSERACT_TESSDATA_PATH="/usr/share/tesseract-ocr/5/tessdata"
# Runs "/usr/bin/dumb-init -- /my/script --with --args"
ENTRYPOINT ["/usr/local/bin/dumb-init", "--"]
CMD ["/usr/src/app/run.sh"]