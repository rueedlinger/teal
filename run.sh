#!/bin/bash

if [ -z ${XDR_WORKERS+x} ]; then
  XDR_WORKERS=1
  echo "env WORKER is unset, will set to $XDR_WORKERS"

else
    echo "env WORKER is set to '$XDR_WORKERS'"
fi

if [ -z ${XDR_PORT+x} ]; then
  XDR_PORT=8000
  echo "env PORT is unset, will set port to $XDR_PORT"
else
  echo "env PORT is set to '$XDR_PORT'"
fi

if [ -z ${XDR_IP_BIND+x} ]; then
  XDR_IP_BIND=0.0.0.0
  echo "env IP is unset, will set IP to $XDR_IP_BIND"
else
  echo "env IP is set to '$XDR_IP_BIND'"
fi


gunicorn xdractify.api:app --workers "$XDR_WORKERS" --worker-class uvicorn.workers.UvicornWorker --bind "$XDR_IP_BIND":"$XDR_PORT" --access-logfile="-" --error-logfile="-"
