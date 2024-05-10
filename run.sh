#!/bin/bash

if [ -z ${XFY_WORKERS+x} ]; then
  XFY_WORKERS=1
  echo "env XFY_WORKERS is unset, will set to $XFY_WORKERS"

else
    echo "env XFY_WORKERS is set to '$XFY_WORKERS'"
fi

if [ -z ${XFY_PORT+x} ]; then
  XFY_PORT=8000
  echo "env XFY_PORT is unset, will set port to $XFY_PORT"
else
  echo "env XFY_PORT is set to '$XFY_PORT'"
fi

if [ -z ${XFY_IP_BIND+x} ]; then
  XFY_IP_BIND=0.0.0.0
  echo "env XFY_IP_BIND is unset, will set IP to $XFY_IP_BIND"
else
  echo "env XDR_IP_BIND is set to '$XFY_IP_BIND'"
fi


gunicorn xfy.api:app --workers "$XFY_WORKERS" \
  --worker-class uvicorn.workers.UvicornWorker --bind "$XFY_IP_BIND":"$XFY_PORT" \
  --access-logfile="-" --error-logfile="-"
