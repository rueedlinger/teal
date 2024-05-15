#!/bin/bash

echo "env TEAL_VERSION is '$TEAL_VERSION'"

if [ "$TEAL_TEST_MODE" = true ] ; then
  echo "env TEAL_TEST_MODE ist set to '$TEAL_TEST_MODE'"
  echo "running in test mode"

  if [ -z ${TEAL_PYTEST_ARGS+x} ]; then
    export COVERAGE_FILE=/tmp/coverage
    pytest --cov=teal --cov-report term-missing --no-header -v --disable-warnings
  else
    pytest $TEAL_PYTEST_ARGS
  fi

  #pytest --no-header -v --disable-warnings --log-cli-level debug
  echo "shutting container down..."
  exit
fi


if [ -z ${TEAL_WORKERS+x} ]; then
  TEAL_WORKERS=1
  echo "env TEAL_WORKERS is unset, will set to $TEAL_WORKERS"

else
    echo "env TEAL_WORKERS is set to '$TEAL_WORKERS'"
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



gunicorn teal.api:app --workers "$TEAL_WORKERS" \
    --worker-class uvicorn.workers.UvicornWorker --bind "$TEAL_IP_BIND":"$TEAL_PORT" \
    --access-logfile="-" --error-logfile="-"


