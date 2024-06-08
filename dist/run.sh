#!/bin/bash

if [ "$TEAL_TEST_MODE" = true ] ; then
  echo "env TEAL_TEST_MODE ist set to '$TEAL_TEST_MODE'"
  echo "running in TEST MODE"

  if [ -z ${TEAL_PYTEST_ARGS+x} ]; then
    export COVERAGE_FILE=/tmp/coverage
    pytest  -vv --cov=teal --cov-report term-missing --cov-report html:$HOME/cov_html --no-header -v --disable-warnings
  else
    pytest $TEAL_PYTEST_ARGS
  fi

  echo "shutting container down..."
  exit
else
  echo "running in APP MODE"
fi


if [ -z ${TEAL_WORKERS+x} ]; then
  TEAL_WORKERS=1
  echo "env TEAL_WORKERS is unset, will set to $TEAL_WORKERS"
else
    echo "env TEAL_WORKERS is set to '$TEAL_WORKERS'"
    if [ "$TEAL_WORKERS" -gt 1 ]; then
      export PROMETHEUS_MULTIPROC_DIR="/tmp/prometheus"
      echo "running in multi worker mode, creating PROMETHEUS_MULTIPROC_DIR $PROMETHEUS_MULTIPROC_DIR"
      echo "CPU and MEM metrics not available in multi worker mode (TEAL_WORKERS > 1)"
      mkdir $PROMETHEUS_MULTIPROC_DIR
    fi
fi

if [ -z ${TEAL_PORT+x} ]; then
  TEAL_PORT=8000
  echo "env TEAL_PORT is unset, will set port to $TEAL_PORT"
else
  echo "env TEAL_PORT is set to '$TEAL_PORT'"
fi

if [ -z ${TEAL_IP_BIND+x} ]; then
  TEAL_IP_BIND=0.0.0.0
  echo "env TEAL_IP_BIND is unset, will set IP to $TEAL_IP_BIND"
else
  echo "env TEAL_IP_BIND is set to '$TEAL_IP_BIND'"
fi

if [ -z ${TEAL_WORKERS_TIMEOUT+x} ]; then
  TEAL_WORKERS_TIMEOUT=120
  echo "env TEAL_WORKERS_TIMEOUT is unset, will set to $TEAL_WORKERS_TIMEOUT"

else
    echo "env TEAL_WORKERS_TIMEOUT is set to '$TEAL_WORKERS_TIMEOUT'"
fi

if [ "$TEAL_START_LOCUST" = true ] ; then
  echo "env TEAL_START_LOCUST ist set to '$TEAL_START_LOCUST'"

  if [ -z ${TEAL_LOCUST_PORT+x} ]; then
    TEAL_LOCUST_PORT=8089
    echo "TEAL_LOCUST_PORT is unset, will set to port $TEAL_LOCUST_PORT"
  else
    echo "env $TEAL_LOCUST_PORT is set to '$$TEAL_LOCUST_PORT'"
  fi

  locust --host http://localhost:$TEAL_PORT --web-port $TEAL_LOCUST_PORT -f tests/locustfile.py &

fi

TEAL_TESSERACT_TESSDATA_PATH=$(find /usr/share -type d -name tessdata | head -n 1)
export TEAL_TESSERACT_TESSDATA_PATH

TEAL_LIBREOFFICE_VERSION=$(libreoffice --version | head -n 1)
export TEAL_LIBREOFFICE_VERSION

TEAL_OCRMYPDF_VERSION_VERSION=$(ocrmypdf --version | head -n 1)
export TEAL_OCRMYPDF_VERSION_VERSION

TEAL_VERAPDF_VERSION=$(verapdf --version | head -n 1)
export TEAL_VERAPDF_VERSION

# from poppler-utils
TEAL_PDFTOPPM_VERSION=$(echo "$(pdftoppm -v 2>&1 >/dev/null)" | head -n 1)
export TEAL_PDFTOPPM_VERSION

# from poppler-utils
TEAL_PDFTOCAIRO_VERSION=$(echo "$(pdftocairo -v 2>&1 >/dev/null)" | head -n 1)
export TEAL_PDFTOCAIRO_VERSION

TEAL_TESSERACT_VERSION=$(tesseract --version | head -n 1)
export TEAL_TESSERACT_VERSION

TEAL_PYTHON_VERSION=$(python --version | head -n 1)
export TEAL_PYTHON_VERSION

TEAL_JAVA_VERSION=$(java --version | head -n 1)
export TEAL_JAVA_VERSION

TEAL_ARCH_NAME=$(uname -m | head -n 1)
export TEAL_ARCH_NAME

TEAL_ARCH_NPROC=$(nproc)
export TEAL_ARCH_NPROC

echo "see API doc http://$TEAL_IP_BIND:$TEAL_PORT/docs"
gunicorn teal.api:app --workers "$TEAL_WORKERS" \
    --worker-class uvicorn.workers.UvicornWorker --bind "$TEAL_IP_BIND":"$TEAL_PORT" \
    --timeout $TEAL_WORKERS_TIMEOUT --access-logfile="-" --error-logfile="-"
