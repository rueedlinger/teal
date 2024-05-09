#!/bin/bash

if [ -z ${WORKERS+x} ]; then
  WORKERS=1
  echo "env WORKER is unset, will set to $WORKERS"

else
    echo "env WORKER is set to '$WORKERS'"
fi

if [ -z ${PORT+x} ]; then
  PORT=8000
  echo "env PORT is unset, will set port to $PORT"
else
  echo "env PORT is set to '$PORT'"
fi


gunicorn xdractify.api:app --workers "$WORKERS" --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:"$PORT" --access-logfile="-" --error-logfile="-"
