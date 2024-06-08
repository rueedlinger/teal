ARG PYTHON_VERSION=3.12
FROM python:$PYTHON_VERSION

ARG USERNAME=worker
ARG USER_UID=1000
ARG USER_GID=$USER_UID
ARG VERSION

# supported tesseract languages https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html
ARG TESSERACT_LANGUAGES="tesseract-ocr-deu tesseract-ocr-fra tesseract-ocr-ita tesseract-ocr-eng tesseract-ocr-por tesseract-ocr-spa"

LABEL org.opencontainers.image.title="Teal" \
      org.opencontainers.image.description="A convenient REST API for working with PDF's." \
      org.opencontainers.image.documentation="https://teal.yax.ch/" \
      org.opencontainers.image.source="https://github.com/rueedlinger/teal"

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /usr/src/app

############################
# install base packages
############################
RUN groupadd --gid $USER_GID $USERNAME &&\
    useradd --uid $USER_UID --gid $USER_GID -m $USERNAME && \
    wget -O /usr/local/bin/dumb-init https://github.com/Yelp/dumb-init/releases/download/v1.2.5/dumb-init_1.2.5_x86_64  &&\
    chmod +x /usr/local/bin/dumb-init && \
    echo "deb http://deb.debian.org/debian bookworm-backports main" >> /etc/apt/sources.list && \
    apt-get update &&\
    apt-get install -y tesseract-ocr \
    $TESSERACT_LANGUAGES \
    poppler-utils \
    ghostscript \
    python3-tk \
    libgl1 \
    ocrmypdf \
    default-jre-headless &&\
    apt-get --no-install-recommends install -y -qq -t bookworm-backports libreoffice  && \
    apt-get install -y -qq -t bookworm-backports libreoffice-java-common  && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

############################
# insatll verapdf
############################
COPY dist/auto-install.xml /tmp
RUN wget -O /tmp/verapdf-installer.zip https://software.verapdf.org/releases/verapdf-installer.zip && \
    unzip -d /tmp /tmp/verapdf-installer.zip && \
    /tmp/verapdf-greenfield-1.26.2/verapdf-install /tmp/auto-install.xml && \
    rm -rf /tmp/*

############################
# install fonts (inspired by gotenberg)
# see https://github.com/gotenberg/gotenberg/blob/main/build/Dockerfile
############################
RUN wget -O /tmp/ttf-mscorefonts-installer_3.8.1_all.deb http://httpredir.debian.org/debian/pool/contrib/m/msttcorefonts/ttf-mscorefonts-installer_3.8.1_all.deb &&\
    apt-get update &&\
    apt-get install -y -qq --no-install-recommends \
    /tmp/ttf-mscorefonts-installer_3.8.1_all.deb \
    culmus \
    fonts-beng \
    fonts-hosny-amiri \
    fonts-lklug-sinhala \
    fonts-lohit-guru \
    fonts-lohit-knda \
    fonts-samyak-gujr \
    fonts-samyak-mlym \
    fonts-samyak-taml \
    fonts-sarai \
    fonts-sil-abyssinica \
    fonts-sil-padauk \
    fonts-telu \
    fonts-thai-tlwg \
    ttf-wqy-zenhei \
    fonts-arphic-ukai \
    fonts-arphic-uming \
    fonts-ipafont-mincho \
    fonts-ipafont-gothic \
    fonts-unfonts-core \
    # LibreOffice recommends.
    fonts-crosextra-caladea \
    fonts-crosextra-carlito \
    fonts-dejavu \
    fonts-dejavu-extra \
    fonts-liberation \
    fonts-liberation2 \
    fonts-linuxlibertine \
    fonts-noto-cjk \
    fonts-noto-core \
    fonts-noto-mono \
    fonts-noto-ui-core \
    fonts-sil-gentium \
    fonts-sil-gentium-basic &&\
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

############################
# prepare app
############################
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
# Runs "/usr/bin/dumb-init -- /my/script --with --args"
ENTRYPOINT ["/usr/local/bin/dumb-init", "--"]
CMD ["/usr/src/app/run.sh"]