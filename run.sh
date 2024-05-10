#!/bin/bash

if [ -z ${XTRA_WORKERS+x} ]; then
  XTRA_WORKERS=1
  echo "env XTRA_WORKERS is unset, will set to $XTRA_WORKERS"

else
    echo "env XTRA_WORKERS is set to '$XTRA_WORKERS'"
fi

if [ -z ${XTRA_PORT+x} ]; then
  XTRA_PORT=8000
  echo "env XFY_PORT is unset, will set port to $XTRA_PORT"
else
  echo "env XFY_PORT is set to '$XTRA_PORT'"
fi

if [ -z ${XTRA_IP_BIND+x} ]; then
  XTRA_IP_BIND=0.0.0.0
  echo "env XTRA_IP_BIND is unset, will set IP to $XTRA_IP_BIND"
else
  echo "env XTRA_IP_BIND is set to '$XTRA_IP_BIND'"
fi


gunicorn xtra.api:app --workers "$XTRA_WORKERS" \
  --worker-class uvicorn.workers.UvicornWorker --bind "$XTRA_IP_BIND":"$XTRA_PORT" \
  --access-logfile="-" --error-logfile="-"
